#!/usr/bin/env python3
"""
The baseline every library has to beat: SQL in the database you already have.

Two candidates, both scored on the same footing as the dedicated engines:

  B1  exact match on a normalized key. What most teams ship first.
  B2  a blocked similarity join with a hand-picked threshold. What most teams
      ship second, after B1 misses too much.

Neither is a strawman. B2 blocks on three keys, compares four fields with
jaro-winkler, weights them by hand, and takes connected components — which is
a fair description of a competent afternoon's work, and is exactly what the
probabilistic engines are claiming to improve on.
"""
import json, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import duckdb  # noqa: E402
import scoring  # noqa: E402

DATA = HERE / "data"
DATASET = sys.argv[1] if len(sys.argv) > 1 else "febrl3"
BLOCKING = sys.argv[2] if len(sys.argv) > 2 else "prefix"
N = {"febrl1": 1000, "febrl3": 5000}[DATASET]
POSSIBLE = N * (N - 1) // 2
CAP = {"blocks": False, "scores": False, "decides": False,
       "clusters": False, "canonicalises": False}



def load_truth_and_pairs(rows, dataset, scoring):
    """febrl1's link file was not exported; the entity column is the same relation."""
    from itertools import combinations
    truth = {r["rec_id"]: r["true_entity"] for r in rows}
    by = {}
    for r in rows:
        by.setdefault(r["true_entity"], []).append(r["rec_id"])
    pairs = scoring._norm_pairs(
        pr for v in by.values() if len(v) > 1 for pr in combinations(sorted(v), 2))
    return truth, pairs


def load(con):
    con.execute(f"CREATE TABLE r AS SELECT * FROM read_csv_auto('{DATA/(DATASET+'.csv')}', all_varchar=true)")
    con.execute("""
        CREATE TABLE n AS SELECT
            rec_id,
            true_entity,
            lower(trim(coalesce(given_name,'')))    AS gn,
            lower(trim(coalesce(surname,'')))       AS sn,
            regexp_replace(coalesce(date_of_birth,''), '[^0-9]', '', 'g') AS dob,
            lower(trim(coalesce(suburb,'')))        AS suburb,
            trim(coalesce(postcode,''))             AS postcode,
            regexp_replace(coalesce(soc_sec_id,''), '[^0-9]', '', 'g') AS ssn
        FROM r
    """)
    truth = {row[0]: row[1] for row in con.execute("SELECT rec_id, true_entity FROM n").fetchall()}
    return truth


def b1_exact(con, truth):
    """Exact match on given_name + surname + date_of_birth."""
    t0 = time.monotonic()
    rows = con.execute("""
        SELECT rec_id, gn || '|' || sn || '|' || dob AS k FROM n
    """).fetchall()
    secs = time.monotonic() - t0
    labels = {rid: k for rid, k in rows}
    pairs = scoring.pairs_from_clusters(labels)
    return {
        "candidate": "SQL baseline B1 — exact match on normalized key",
        "capabilities": {**CAP, "blocks": True, "decides": True, "clusters": True},
        "capability_note": "Blocking, deciding and clustering are the same GROUP BY. "
                           "There is no score, so there is no threshold to tune and no "
                           "way to trade precision for recall.",
        "seconds": round(secs, 3),
        "pairwise": scoring.pairwise(pairs, TRUE_PAIRS),
        "cluster": scoring.cluster_metrics(truth, labels),
    }


def b2_fuzzy(con, truth, threshold=0.88):
    """Blocked similarity join, hand-weighted, connected components."""
    t0 = time.monotonic()
    # Three blocking keys, unioned. Any one agreeing is enough to be compared.
    con.execute("""
        CREATE OR REPLACE TABLE cand AS
        SELECT DISTINCT least(a.rec_id, b.rec_id) AS id1, greatest(a.rec_id, b.rec_id) AS id2
        FROM n a JOIN n b
          ON a.rec_id < b.rec_id
         AND (   (a.dob = b.dob AND a.dob <> '')
              OR ({pc_rule})
              OR ({sn_rule}) )
    """.format(
        pc_rule=("a.postcode = b.postcode AND a.postcode <> '' AND substr(a.sn,1,2) = substr(b.sn,1,2)"
                 if BLOCKING == "prefix" else
                 "a.postcode = b.postcode AND a.postcode <> '' AND a.sn = b.sn"),
        sn_rule=("a.sn = b.sn AND a.sn <> '' AND substr(a.gn,1,1) = substr(b.gn,1,1)"
                 if BLOCKING == "prefix" else
                 "a.sn = b.sn AND a.sn <> '' AND a.gn = b.gn"),
    ))
    n_cand = con.execute("SELECT count(*) FROM cand").fetchone()[0]
    block_secs = time.monotonic() - t0

    t1 = time.monotonic()
    scored = con.execute("""
        SELECT c.id1, c.id2,
               ( 0.30 * jaro_winkler_similarity(a.gn, b.gn)
               + 0.30 * jaro_winkler_similarity(a.sn, b.sn)
               + 0.25 * (CASE WHEN a.dob = b.dob AND a.dob <> '' THEN 1.0
                              ELSE jaro_winkler_similarity(a.dob, b.dob) END)
               + 0.15 * jaro_winkler_similarity(a.suburb, b.suburb) ) AS score
        FROM cand c JOIN n a ON a.rec_id = c.id1 JOIN n b ON b.rec_id = c.id2
    """).fetchall()
    score_secs = time.monotonic() - t1

    # Blocking recall: the ceiling nothing downstream can lift.
    cand_pairs = {(a, b) for a, b, _ in scored}
    blocking_recall = len(cand_pairs & TRUE_PAIRS) / len(TRUE_PAIRS)

    accepted = [(a, b) for a, b, s in scored if s >= threshold]
    labels = scoring.clusters_from_pairs(accepted, list(truth))
    return {
        "candidate": f"SQL baseline B2 — blocked jaro-winkler join, threshold {threshold}",
        "capabilities": {"blocks": True, "scores": True, "decides": True,
                         "clusters": True, "canonicalises": False},
        "capability_note": "Every step is written by the caller. The threshold is a "
                           "constant chosen by looking at a histogram; nothing estimated it.",
        "threshold": threshold,
        "seconds": round(block_secs + score_secs, 3),
        "blocking": {"candidate_pairs": n_cand,
                     "possible_pairs": POSSIBLE,
                     "reduction_ratio": round(1 - n_cand / POSSIBLE, 6),
                     "blocking_recall": round(blocking_recall, 4),
                     "seconds": round(block_secs, 3)},
        "pairwise": scoring.pairwise(accepted, TRUE_PAIRS),
        "cluster": scoring.cluster_metrics(truth, labels),
    }


if __name__ == "__main__":
    con = duckdb.connect()
    truth = load(con)
    import csv as _csv
    with (DATA / f"{DATASET}.csv").open(newline="") as fh:
        _rows = list(_csv.DictReader(fh))
    _, TRUE_PAIRS = load_truth_and_pairs(_rows, DATASET, scoring)
    out = {"probe": "duckdb", "duckdb_version": duckdb.__version__,
           "dataset": DATASET, "blocking_variant": BLOCKING, "results": [b1_exact(con, truth)]}
    for th in (0.80, 0.85, 0.88, 0.92):
        out["results"].append(b2_fuzzy(con, truth, th))
    print(json.dumps(out, indent=2))
