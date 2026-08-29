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

# The LINTERS, added for 1.250. Same pinning discipline. Versions read from PyPI and the
# npm registry on 2026-08-29, the day 1.250's S1 was written, so the survey's adoption
# table and its benchmark describe the same releases.
#
# Pylint is here to be TIMED, not to be raced: nothing else in the category does
# whole-program inference, so there is no matched rule set and therefore no honest ratio.
RUN pip install --no-cache-dir \
        flake8==7.3.0 \
        pylint==4.0.8

# oxlint and biome are Rust; eslint is JavaScript linting JavaScript. Biome appears twice
# in this image at two majors — 1.9.4 is what 1.253 measured for FORMATTING and must not
# move, so the linter is pinned separately as 2.5.11 and invoked from its own path.
RUN npm install -g --no-fund --no-audit \
        eslint@10.9.1 \
        oxlint@1.80.0 \
    && npm install -g --no-fund --no-audit --prefix /opt/biome2 @biomejs/biome@2.5.11

WORKDIR /bench
COPY bench.py bench_lint.py corpus.json eslint.config.mjs ./
ENTRYPOINT ["python3", "bench.py"]
