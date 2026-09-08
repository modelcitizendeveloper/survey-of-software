#!/usr/bin/env python3
"""
recordlinkage: the toolkit tier.

Blocks, compares, classifies — and then hands back a MultiIndex of pairs. The
probe records where the library stops and what the caller has to do next, which
is the survey's whole question.

The classifier is the ECM (expectation-maximisation Fellegi-Sunter) estimator,
because it is the unsupervised one: it needs no labels, which makes it the fair
comparison against Splink's EM and against the SQL baseline. The supervised
classifiers would need training pairs the baseline never gets.
"""
import json, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import pandas as pd  # noqa: E402
import recordlinkage as rl  # noqa: E402
import scoring  # noqa: E402

DATA = HERE / "data"
DATASET = sys.argv[1] if len(sys.argv) > 1 else "febrl3"
# "exact"  : block on whole field values — the obvious first choice
# "prefix" : same three keys, two of them loosened to a prefix
BLOCKING = sys.argv[2] if len(sys.argv) > 2 else "prefix"
N = {"febrl1": 1000, "febrl3": 5000}[DATASET]
POSSIBLE = N * (N - 1) // 2


def main():
    df = pd.read_csv(DATA / f"{DATASET}.csv", dtype=str).fillna("")
    df = df.set_index("rec_id")
    # Same three blocking keys as the SQL baseline, so the comparison is not decided
    # by whose blocking rules the author happened to write better.
    df["sn2"] = df["surname"].str[:2]
    df["gn1"] = df["given_name"].str[:1]
    truth = df["true_entity"].to_dict()
    from itertools import combinations
    _by = {}
    for _rid, _ent in truth.items():
        _by.setdefault(_ent, []).append(_rid)
    true_pairs = scoring._norm_pairs(
        pr for v in _by.values() if len(v) > 1 for pr in combinations(sorted(v), 2))

    t0 = time.monotonic()
    indexer = rl.Index()
    indexer.block("date_of_birth")
    if BLOCKING == "prefix":
        indexer.block(["postcode", "sn2"])
        indexer.block(["surname", "gn1"])
    else:
        indexer.block(["postcode", "surname"])
        indexer.block(["surname", "given_name"])
    cand = indexer.index(df)
    block_secs = time.monotonic() - t0
    cand_pairs = scoring._norm_pairs(cand)
    blocking_recall = len(cand_pairs & true_pairs) / len(true_pairs)

    t1 = time.monotonic()
    cmp = rl.Compare()
    cmp.string("given_name", "given_name", method="jarowinkler", label="given_name")
    cmp.string("surname", "surname", method="jarowinkler", label="surname")
    cmp.exact("date_of_birth", "date_of_birth", label="date_of_birth")
    cmp.string("suburb", "suburb", method="jarowinkler", label="suburb")
    cmp.exact("postcode", "postcode", label="postcode")
    cmp.string("address_1", "address_1", method="jarowinkler", label="address_1")
    features = cmp.compute(cand, df)
    compare_secs = time.monotonic() - t1

    results = []
    # ECM: unsupervised Fellegi-Sunter. No labels supplied.
    t2 = time.monotonic()
    ecm = rl.ECMClassifier(binarize=0.85)
    matches = ecm.fit_predict(features)
    ecm_secs = time.monotonic() - t2
    accepted = scoring._norm_pairs(matches)
    # The library returns pairs. The caller does this next, and it is not free.
    labels = scoring.clusters_from_pairs(accepted, list(truth))
    results.append({
        "classifier": "ECMClassifier (unsupervised Fellegi-Sunter, binarize=0.85)",
        "seconds": round(ecm_secs, 3),
        "pairwise": scoring.pairwise(accepted, true_pairs),
        "cluster_via_caller_connected_components": scoring.cluster_metrics(truth, labels),
    })

    # A simple sum-of-features threshold, for comparison with the SQL baseline's
    # hand-weighted score: same idea, different framework.
    for th in (4.0, 4.5, 5.0):
        acc = scoring._norm_pairs(features[features.sum(axis=1) >= th].index)
        lab = scoring.clusters_from_pairs(acc, list(truth))
        results.append({
            "classifier": f"sum of comparison vector >= {th} (no model)",
            "seconds": None,
            "pairwise": scoring.pairwise(acc, true_pairs),
            "cluster_via_caller_connected_components": scoring.cluster_metrics(truth, lab),
        })

    print(json.dumps({
        "probe": "recordlinkage",
        "version": rl.__version__,
        "dataset": DATASET,
        "blocking_variant": BLOCKING,
        "capabilities": {"blocks": True, "scores": True, "decides": True,
                         "clusters": False, "canonicalises": False},
        "capability_note": "Returns a pandas MultiIndex of matched pairs. There is no "
                           "clustering step in the library; the partition below was "
                           "produced by the probe taking connected components, which is "
                           "what a caller does and is where a single false pair welds two "
                           "entities together.",
        "blocking": {"candidate_pairs": len(cand),
                     "possible_pairs": POSSIBLE,
                     "reduction_ratio": round(1 - len(cand) / POSSIBLE, 6),
                     "blocking_recall": round(blocking_recall, 4),
                     "seconds": round(block_secs, 3)},
        "compare_seconds": round(compare_secs, 3),
        "results": results,
    }, indent=2))


if __name__ == "__main__":
    main()
