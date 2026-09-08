#!/usr/bin/env python3
"""
dedupe: the one that finishes the job.

It is the only candidate measured here that does all five things — blocks,
scores, decides, clusters AND canonicalises — and the only one whose clustering
is not connected components: `cluster()` uses hierarchical clustering and keeps a
cluster only if its cophenetic similarity clears the threshold, which by
construction refuses the A-B-C chain that connected components accepts.

TWO SUBSTITUTIONS, BOTH DECLARED.

1. dedupe is built around active learning: it proposes uncertain pairs and a
   human answers. The probe answers dedupe's own uncertain_pairs() from FEBRL's
   ground truth. This is dedupe's interaction with a PERFECT oracle, so read the
   result as a ceiling on the human loop, not a prediction of it.

2. Scoring is done ONCE and clustered at four thresholds, rather than calling
   partition() four times. partition() is pairs -> score -> cluster and would
   repeat the expensive two-thirds; the arithmetic is identical.

in_memory is left at the library default (False, SQLite-backed). An earlier run
with in_memory=True reached 9.4 GiB resident on 5,000 records and was killed.
"""
import csv, json, resource, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import dedupe  # noqa: E402
from dedupe import variables  # noqa: E402
import scoring  # noqa: E402

DATA = HERE / "data"
LABEL_ROUNDS = 40

# Address-space cap. An uncapped run on febrl3 reached 7.9 GiB resident at
# library defaults and had to be killed; a cap turns that into a clean,
# reportable MemoryError instead of a swapping machine. 6 GiB is generous
# against splink's 191 MiB venv doing the same job in 2.2 seconds.
MEM_CAP_BYTES = 6 * 1024**3
resource.setrlimit(resource.RLIMIT_AS, (MEM_CAP_BYTES, MEM_CAP_BYTES))

DATASET = sys.argv[1] if len(sys.argv) > 1 else "febrl3"
POSSIBLE = {"febrl1": 1000 * 999 // 2, "febrl3": 5000 * 4999 // 2}[DATASET]


def main():
    with (DATA / f"{DATASET}.csv").open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    truth = {r["rec_id"]: r["true_entity"] for r in rows}
    if DATASET == "febrl3":
        with (DATA / "febrl3_links.csv").open(newline="") as fh:
            true_pairs = scoring._norm_pairs((r["id_1"], r["id_2"]) for r in csv.DictReader(fh))
    else:
        # febrl1's links were not exported separately; derive from the ground-truth
        # entity, which is the same relation by construction.
        by = {}
        for r in rows:
            by.setdefault(r["true_entity"], []).append(r["rec_id"])
        from itertools import combinations
        true_pairs = scoring._norm_pairs(
            pr for v in by.values() if len(v) > 1 for pr in combinations(sorted(v), 2))

    fields = ["given_name", "surname", "date_of_birth", "suburb", "postcode", "address_1"]
    data = {r["rec_id"]: {f: (r[f] or None) for f in fields} for r in rows}

    var_defs = [
        variables.String("given_name", has_missing=True),
        variables.String("surname", has_missing=True),
        variables.Exact("date_of_birth", has_missing=True),
        variables.String("suburb", has_missing=True),
        variables.Exact("postcode", has_missing=True),
        variables.String("address_1", has_missing=True),
    ]

    t0 = time.monotonic()
    deduper = dedupe.Dedupe(var_defs)
    deduper.prepare_training(data)
    rev = {id(v): k for k, v in data.items()}
    asked = matched = 0
    for _ in range(LABEL_ROUNDS):
        pairs = deduper.uncertain_pairs()
        if not pairs:
            break
        labelled = {"match": [], "distinct": []}
        for a, b in pairs:
            ka, kb = rev.get(id(a)), rev.get(id(b))
            if ka is None or kb is None:
                continue
            same = truth[ka] == truth[kb]
            labelled["match" if same else "distinct"].append((a, b))
            asked += 1
            matched += same
        deduper.mark_pairs(labelled)
    deduper.train()
    train_secs = time.monotonic() - t0

    t1 = time.monotonic()
    pair_iter = deduper.pairs(data)
    scores = deduper.score(pair_iter)
    score_secs = time.monotonic() - t1
    n_scored = len(scores)
    cand_pairs = scoring._norm_pairs(tuple(p) for p in scores["pairs"])
    blocking_recall = len(cand_pairs & true_pairs) / len(true_pairs)

    results = []
    for th in (0.3, 0.5, 0.7, 0.9):
        t2 = time.monotonic()
        clusters = list(deduper.cluster(scores, threshold=th))
        cl_secs = time.monotonic() - t2
        labels, seen = {}, set()
        for cid, (recs, _s) in enumerate(clusters):
            for rid in recs:
                labels[rid] = f"c{cid}"
                seen.add(rid)
        for rid in data:                       # singletons, as partition() adds them
            if rid not in seen:
                labels[rid] = f"s{rid}"
        pairs_pred = scoring.pairs_from_clusters(labels)
        labels_cc = scoring.clusters_from_pairs(
            [tuple(p) for p, s in zip(scores["pairs"], scores["score"]) if s >= th], list(truth))
        results.append({
            "threshold": th,
            "cluster_seconds": round(cl_secs, 3),
            "pairwise": scoring.pairwise(pairs_pred, true_pairs),
            "cluster_dedupe_hierarchical": scoring.cluster_metrics(truth, labels),
            "cluster_naive_connected_components": scoring.cluster_metrics(truth, labels_cc),
        })

    # canonicalisation: one canonical record from the largest cluster found at 0.5
    canon = None
    best = max((c for c in list(deduper.cluster(scores, threshold=0.5))),
               key=lambda c: len(c[0]), default=None)
    if best is not None:
        canon = {"cluster_records": [{"rec_id": r, **data[r]} for r in best[0]],
                 "canonical": dedupe.canonicalize([data[r] for r in best[0]])}

    print(json.dumps({
        "probe": "dedupe",
        "version": "3.0.3",
        "btrees_pinned": "6.4 — 6.5 removed byValue() and breaks dedupe at blocking time",
        "dataset": DATASET,
        "capabilities": {"blocks": True, "scores": True, "decides": True,
                         "clusters": True, "canonicalises": True},
        "capability_note": "The only candidate measured that canonicalises, and the only "
                           "one whose clustering is hierarchical rather than connected "
                           "components. Both partitions are reported.",
        "training": {"style": "active learning, oracle-answered from ground truth",
                     "labels_supplied": asked, "of_which_matches": matched,
                     "seconds": round(train_secs, 3),
                     "caveat": "a perfect oracle is a ceiling on the human loop"},
        "scoring": {"pairs_scored": int(n_scored), "seconds": round(score_secs, 3),
                    "possible_pairs": POSSIBLE,
                    "reduction_ratio": round(1 - n_scored / POSSIBLE, 6),
                    "blocking_recall": round(blocking_recall, 4)},
        "peak_rss_mib": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1),
        "address_space_cap_mib": MEM_CAP_BYTES // 1048576,
        "results": results,
        "canonicalisation_example": canon,
    }, indent=2, default=str))


if __name__ == "__main__":
    main()
