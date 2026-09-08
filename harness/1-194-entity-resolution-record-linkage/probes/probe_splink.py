#!/usr/bin/env python3
"""
Splink: the only candidate that performs all four steps under one API.

Trained without labels, as the documentation says it can be: u-probabilities by
random sampling, m-probabilities by expectation-maximisation on two blocked
passes. The probe supplies no ground truth to the model at any point.

The clustering step is Splink's own, not the probe's — which is the difference
this survey is built on, so the probe also records what connected components
over the same accepted pairs would have produced.
"""
import json, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import pandas as pd  # noqa: E402
import splink  # noqa: E402
from splink import DuckDBAPI, Linker, SettingsCreator, block_on  # noqa: E402
import splink.comparison_library as cl  # noqa: E402
import scoring  # noqa: E402

DATA = HERE / "data"
DATASET = sys.argv[1] if len(sys.argv) > 1 else "febrl3"
BLOCKING = sys.argv[2] if len(sys.argv) > 2 else "prefix"
N = {"febrl1": 1000, "febrl3": 5000}[DATASET]
POSSIBLE = N * (N - 1) // 2


def main():
    df = pd.read_csv(DATA / f"{DATASET}.csv", dtype=str).fillna("")
    df = df.rename(columns={"rec_id": "unique_id"})
    truth = dict(zip(df["unique_id"], df["true_entity"]))
    from itertools import combinations
    _by = {}
    for _rid, _ent in truth.items():
        _by.setdefault(_ent, []).append(_rid)
    true_pairs = scoring._norm_pairs(
        pr for v in _by.values() if len(v) > 1 for pr in combinations(sorted(v), 2))

    settings = SettingsCreator(
        link_type="dedupe_only",
        comparisons=[
            cl.JaroWinklerAtThresholds("given_name", [0.9, 0.8]),
            cl.JaroWinklerAtThresholds("surname", [0.9, 0.8]),
            cl.DamerauLevenshteinAtThresholds("date_of_birth", [1, 2]),
            cl.JaroWinklerAtThresholds("suburb", [0.9]),
            cl.ExactMatch("postcode"),
            cl.JaroWinklerAtThresholds("address_1", [0.9, 0.8]),
        ],
        blocking_rules_to_generate_predictions=[
            # Same three blocking keys as the SQL baseline, in two variants.
            block_on("date_of_birth"),
            *( [block_on("postcode", "substr(surname,1,2)"),
                block_on("surname", "substr(given_name,1,1)")]
               if BLOCKING == "prefix" else
               [block_on("postcode", "surname"), block_on("surname", "given_name")] ),
        ],
        retain_intermediate_calculation_columns=False,
    )

    t0 = time.monotonic()
    linker = Linker(df, settings, db_api=DuckDBAPI())
    linker.training.estimate_probability_two_random_records_match(
        [block_on("date_of_birth", "surname"), block_on("given_name", "surname", "postcode")],
        recall=0.8,
    )
    linker.training.estimate_u_using_random_sampling(max_pairs=2e6)
    linker.training.estimate_parameters_using_expectation_maximisation(block_on("date_of_birth"))
    linker.training.estimate_parameters_using_expectation_maximisation(block_on("surname", "given_name"))
    train_secs = time.monotonic() - t0

    t1 = time.monotonic()
    preds = linker.inference.predict()
    pdf = preds.as_pandas_dataframe()
    predict_secs = time.monotonic() - t1

    cand_pairs = scoring._norm_pairs(zip(pdf["unique_id_l"], pdf["unique_id_r"]))
    blocking_recall = len(cand_pairs & true_pairs) / len(true_pairs)

    results = []
    for th in (0.5, 0.9, 0.95, 0.99):
        t2 = time.monotonic()
        cl_res = linker.clustering.cluster_pairwise_predictions_at_threshold(
            preds, threshold_match_probability=th)
        cdf = cl_res.as_pandas_dataframe()
        cluster_secs = time.monotonic() - t2
        labels_splink = dict(zip(cdf["unique_id"], cdf["cluster_id"]))
        accepted = scoring._norm_pairs(
            zip(pdf.loc[pdf["match_probability"] >= th, "unique_id_l"],
                pdf.loc[pdf["match_probability"] >= th, "unique_id_r"]))
        labels_cc = scoring.clusters_from_pairs(accepted, list(truth))
        results.append({
            "threshold_match_probability": th,
            "cluster_seconds": round(cluster_secs, 3),
            "pairwise": scoring.pairwise(accepted, true_pairs),
            "cluster_splink_own": scoring.cluster_metrics(truth, labels_splink),
            "cluster_naive_connected_components": scoring.cluster_metrics(truth, labels_cc),
        })

    print(json.dumps({
        "probe": "splink",
        "version": splink.__version__,
        "backend": "DuckDBAPI (in-process)",
        "dataset": DATASET,
        "blocking_variant": BLOCKING,
        "capabilities": {"blocks": True, "scores": True, "decides": True,
                         "clusters": True, "canonicalises": False},
        "capability_note": "Trained with no labelled pairs. Clustering is the library's "
                           "own step, run at each threshold; the naive connected-components "
                           "partition over the same accepted pairs is reported beside it.",
        "training_seconds": round(train_secs, 3),
        "predict_seconds": round(predict_secs, 3),
        "blocking": {"candidate_pairs": int(len(pdf)),
                     "possible_pairs": POSSIBLE,
                     "reduction_ratio": round(1 - len(pdf) / POSSIBLE, 6),
                     "blocking_recall": round(blocking_recall, 4)},
        "results": results,
    }, indent=2))


if __name__ == "__main__":
    main()
