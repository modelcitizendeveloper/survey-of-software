#!/usr/bin/env python3
"""
Download Stanza models for Latin NLP pipeline
"""

print("Downloading Stanza Latin models...")
print("This will download ~100MB of data to ~/stanza_resources/")

try:
    import stanza

    # Download Latin models
    stanza.download('la', verbose=True)

    print("\n✓ Stanza models downloaded successfully!")
    print("Location: ~/stanza_resources/la/")

except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    print("\nTrying alternative download method via CLTK...")

    try:
        from cltk.data.fetch import FetchCorpus

        corpus_downloader = FetchCorpus(language="lat")

        # List available corpora
        print("\nAvailable Latin corpora:")
        for corpus in corpus_downloader.list_corpora:
            print(f"  - {corpus}")

        # Try to download stanza models if available
        if "lat_models_stanza" in corpus_downloader.list_corpora:
            print("\nDownloading lat_models_stanza...")
            corpus_downloader.import_corpus("lat_models_stanza")
            print("✓ Downloaded via CLTK!")

    except Exception as e2:
        print(f"✗ CLTK download also failed: {type(e2).__name__}: {e2}")
