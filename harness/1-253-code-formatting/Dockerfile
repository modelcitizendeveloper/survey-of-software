# Harness for 1.253 Code Formatting Libraries — a `measured-local` rung.
#
# Pinned all the way down. A benchmark whose tool versions float measures a different thing
# every time it runs, which is the failure this whole harness exists to correct.
FROM python:3.12.11-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates procps \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# The Python formatters under test. Every version is exact — including the ones that lose.
#
# `blue` is ABSENT and that is a finding, not an omission: blue 0.9.1 pins black==22.1.0,
# so it cannot be installed beside a current Black at all. 1.253 says of it "Nothing new;
# move existing users to Ruff" — the dependency pin says the same thing more plainly.
RUN pip install --no-cache-dir \
        ruff==0.16.5 \
        black==26.5.1 \
        autopep8==2.3.2 \
        yapf==0.43.0

# The JavaScript formatters. Biome and dprint are Rust binaries; that is the whole point of
# the comparison, and the reason none of this can run in a browser.
RUN npm install -g --no-fund --no-audit \
        prettier@3.4.2 \
        @biomejs/biome@1.9.4 \
        dprint@0.47.6

WORKDIR /bench
COPY bench.py corpus.json ./
ENTRYPOINT ["python3", "bench.py"]
