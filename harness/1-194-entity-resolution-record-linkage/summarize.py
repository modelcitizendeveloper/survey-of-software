#!/usr/bin/env python3
"""One table per dataset, from the committed probe JSON. No numbers are retyped."""
import json
from pathlib import Path
R = Path(__file__).parent / "results"


def rows_for(ds):
    out = []
    f = R / f"probe_duckdb_{ds}.json"
    if f.exists():
        d = json.loads(f.read_text())
        for r in d["results"]:
            b = r.get("blocking", {})
            out.append(("SQL/DuckDB", r["candidate"].split("—")[1].strip(), r["seconds"],
                        r["pairwise"], r["cluster"], b.get("blocking_recall"),
                        b.get("candidate_pairs")))
    f = R / f"probe_recordlinkage_{ds}.json"
    if f.exists():
        d = json.loads(f.read_text())
        b = d["blocking"]
        for r in d["results"]:
            out.append(("recordlinkage", r["classifier"][:44], r["seconds"], r["pairwise"],
                        r["cluster_via_caller_connected_components"],
                        b["blocking_recall"], b["candidate_pairs"]))
    f = R / f"probe_splink_{ds}.json"
    if f.exists():
        d = json.loads(f.read_text())
        b = d["blocking"]
        for r in d["results"]:
            out.append(("splink", f"threshold {r['threshold_match_probability']}",
                        d["training_seconds"] + d["predict_seconds"], r["pairwise"],
                        r["cluster_splink_own"], b["blocking_recall"], b["candidate_pairs"]))
    f = R / f"probe_dedupe_{ds}.json"
    if f.exists():
        d = json.loads(f.read_text())
        if d.get("outcome") == "MemoryError":
            out.append(("dedupe", "MemoryError at 6 GiB during prepare_training",
                        None, None, None, None, None))
        else:
            s = d["scoring"]
            for r in d["results"]:
                out.append(("dedupe", f"threshold {r['threshold']}",
                            d["training"]["seconds"] + s["seconds"], r["pairwise"],
                            r["cluster_dedupe_hierarchical"], s["blocking_recall"],
                            s["pairs_scored"]))
    return out


for ds in ("febrl1", "febrl3"):
    meta = json.loads((Path(__file__).parent / "data" / "meta.json").read_text())["sets"][ds]
    print(f"\n{'='*118}\n{ds}: {meta['records']} records, "
          f"{meta.get('true_entities')} true entities, {meta['true_pairs']} true pairs, "
          f"{meta.get('possible_pairs') or meta['records']*(meta['records']-1)//2:,} possible pairs\n{'='*118}")
    print(f"{'tool':14s} {'operating point':46s} {'secs':>7s} {'P':>6s} {'R':>6s} {'F1':>6s} "
          f"{'ents':>6s} {'exact':>6s} {'ARI':>6s} {'blkR':>5s}")
    for tool, op, secs, pw, cl, br, cand in rows_for(ds):
        if pw is None:
            print(f"{tool:14s} {op:46s} {'—':>7s}")
            continue
        secs_s = f"{secs:7.2f}" if secs is not None else "      —"
        print(f"{tool:14s} {op:46s} {secs_s} {pw['precision']:>6.3f} {pw['recall']:>6.3f} "
              f"{pw['f1']:>6.3f} {cl['predicted_entities']:>6d} "
              f"{cl['exact_recovery_rate']:>6.3f} {cl['adjusted_rand_index']:>6.3f} "
              f"{(br if br is not None else 0):>5.3f}")
