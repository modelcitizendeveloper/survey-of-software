#!/usr/bin/env python3
"""
Freeze the benchmark to CSV so every probe reads identical bytes.

FEBRL ships inside `recordlinkage`, which is one of the candidates. Loading it
from there inside each probe would make the benchmark a dependency of the thing
being benchmarked, and would silently change if that package changed. Exporting
once fixes both.

Run with the recordlinkage venv:
    .venvs/recordlinkage-3.12/bin/python export_data.py
"""
import hashlib, json
from pathlib import Path
import pandas as pd
import recordlinkage
from recordlinkage import datasets as ds

OUT = Path(__file__).parent / "data"
OUT.mkdir(exist_ok=True)
meta = {"recordlinkage_version": recordlinkage.__version__, "sets": {}}


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


# --- FEBRL3: deduplication. 5,000 records, 2,000 entities, clusters of 1..6 ---
df, links = ds.load_febrl3(return_links=True)
df = df.reset_index()
# Ground-truth entity id is encoded in the record id: rec-<n>-org / rec-<n>-dup-<k>
df["true_entity"] = df["rec_id"].str.extract(r"^rec-(\d+)-")[0]
df.to_csv(OUT / "febrl3.csv", index=False)
pd.DataFrame(list(links), columns=["id_1", "id_2"]).to_csv(OUT / "febrl3_links.csv", index=False)
meta["sets"]["febrl3"] = {
    "task": "deduplication (one table)",
    "records": int(len(df)),
    "true_entities": int(df["true_entity"].nunique()),
    "true_pairs": int(len(links)),
    "possible_pairs": int(len(df) * (len(df) - 1) // 2),
    "cluster_sizes": {str(k): int(v) for k, v in
                      df.groupby("true_entity").size().value_counts().sort_index().items()},
    "sha256_16": digest(OUT / "febrl3.csv"),
}

# --- FEBRL4: linkage. 5,000 x 5,000, 5,000 true one-to-one links ---
a, b, links4 = ds.load_febrl4(return_links=True)
a = a.reset_index(); b = b.reset_index()
a.to_csv(OUT / "febrl4_a.csv", index=False)
b.to_csv(OUT / "febrl4_b.csv", index=False)
pd.DataFrame(list(links4), columns=["id_a", "id_b"]).to_csv(OUT / "febrl4_links.csv", index=False)
meta["sets"]["febrl4"] = {
    "task": "linkage (two tables)",
    "records_a": int(len(a)), "records_b": int(len(b)),
    "true_pairs": int(len(links4)),
    "possible_pairs": int(len(a) * len(b)),
    "sha256_16_a": digest(OUT / "febrl4_a.csv"),
    "sha256_16_b": digest(OUT / "febrl4_b.csv"),
}

# --- FEBRL1: 1,000 records. Small enough for anything, including a 500-record cut ---
df1, links1 = ds.load_febrl1(return_links=True)
df1 = df1.reset_index()
df1["true_entity"] = df1["rec_id"].str.extract(r"^rec-(\d+)-")[0]
df1.to_csv(OUT / "febrl1.csv", index=False)
meta["sets"]["febrl1"] = {"records": int(len(df1)), "true_pairs": int(len(links1)),
                          "true_entities": int(df1["true_entity"].nunique()),
                          "sha256_16": digest(OUT / "febrl1.csv")}

Path(OUT / "meta.json").write_text(json.dumps(meta, indent=2))
print(json.dumps(meta, indent=2))
