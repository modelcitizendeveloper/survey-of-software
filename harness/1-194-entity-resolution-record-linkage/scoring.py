"""
One scorer, imported by every probe, so no candidate is scored on its own terms.

Pure stdlib on purpose: it has to import inside eleven different virtual
environments whose dependency sets have nothing in common.

Two families of number, kept apart deliberately:

  PAIRWISE   over the set of record pairs asserted to be the same entity.
             This is what most of the field reports.

  CLUSTER    over the partition of records into entities. This is what a caller
             writing one row per entity actually gets, and it is not derivable
             from the pairwise score: a single false pair can weld two true
             entities together, costing one pair of precision and two entities.

Reporting only the first flatters every tool that stops before clustering, which
is why both are computed for anything that reaches a partition.
"""
from collections import Counter
from itertools import combinations
from math import comb


def _norm_pairs(pairs):
    return {(a, b) if a <= b else (b, a) for a, b in pairs}


def pairwise(predicted_pairs, true_pairs):
    """Precision / recall / F1 over asserted same-entity pairs."""
    p = _norm_pairs(predicted_pairs)
    t = _norm_pairs(true_pairs)
    tp = len(p & t)
    fp = len(p - t)
    fn = len(t - p)
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    return {"tp": tp, "fp": fp, "fn": fn,
            "precision": round(prec, 4), "recall": round(rec, 4), "f1": round(f1, 4),
            "predicted_pairs": len(p), "true_pairs": len(t)}


def pairs_from_clusters(labels):
    """All within-cluster pairs implied by a {record_id: cluster_id} mapping."""
    groups = {}
    for rid, cid in labels.items():
        groups.setdefault(cid, []).append(rid)
    out = set()
    for members in groups.values():
        if len(members) > 1:
            out.update((a, b) if a <= b else (b, a) for a, b in combinations(sorted(members), 2))
    return out


def adjusted_rand(labels_true, labels_pred, keys):
    """ARI without sklearn. 1.0 is a perfect partition; ~0.0 is chance."""
    cont = Counter((labels_true[k], labels_pred[k]) for k in keys)
    a = Counter(labels_true[k] for k in keys)
    b = Counter(labels_pred[k] for k in keys)
    n = len(keys)
    sum_ij = sum(comb(v, 2) for v in cont.values())
    sum_a = sum(comb(v, 2) for v in a.values())
    sum_b = sum(comb(v, 2) for v in b.values())
    total = comb(n, 2)
    if total == 0:
        return 0.0
    expected = sum_a * sum_b / total
    maximum = (sum_a + sum_b) / 2
    return round((sum_ij - expected) / (maximum - expected), 4) if maximum != expected else 1.0


def cluster_metrics(labels_true, labels_pred):
    """
    Partition-level agreement.

    `exact_entities_recovered` is the number a caller feels: how many real
    entities came back as exactly the right set of records, no more and no less.
    """
    keys = [k for k in labels_true if k in labels_pred]
    true_groups, pred_groups = {}, {}
    for k in keys:
        true_groups.setdefault(labels_true[k], set()).add(k)
        pred_groups.setdefault(labels_pred[k], set()).add(k)
    pred_sets = {frozenset(v) for v in pred_groups.values()}
    exact = sum(1 for v in true_groups.values() if frozenset(v) in pred_sets)
    return {
        "true_entities": len(true_groups),
        "predicted_entities": len(pred_groups),
        "exact_entities_recovered": exact,
        "exact_recovery_rate": round(exact / len(true_groups), 4) if true_groups else 0.0,
        "adjusted_rand_index": adjusted_rand(labels_true, labels_pred, keys),
        "records_scored": len(keys),
    }


def clusters_from_pairs(pairs, all_ids):
    """
    Connected components — the transitive closure a caller performs when the
    library returns pairs and stops. Included so the cost of doing it naively is
    measured rather than assumed: it is the default, and it is where one wrong
    pair becomes one wrong entity.
    """
    parent = {i: i for i in all_ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in pairs:
        if a in parent and b in parent:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
    return {i: find(i) for i in all_ids}
