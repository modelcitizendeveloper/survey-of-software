#!/usr/bin/env python3
"""
Download all available Latin corpora from CLTK
"""

from cltk.data.fetch import FetchCorpus

corpus_downloader = FetchCorpus(language="lat")

print("Available Latin corpora:")
print("=" * 70)
for corpus in corpus_downloader.list_corpora:
    print(f"  - {corpus}")

print("\n" + "=" * 70)
print("Downloading all available Latin corpora...")
print("=" * 70)

for corpus in corpus_downloader.list_corpora:
    print(f"\nDownloading: {corpus}...")
    try:
        corpus_downloader.import_corpus(corpus)
        print(f"  ✓ {corpus} downloaded successfully!")
    except Exception as e:
        print(f"  ✗ {corpus} failed: {type(e).__name__}: {e}")

print("\n" + "=" * 70)
print("Download complete!")
print("=" * 70)
