---
title: "What Changed"
description: "Which surveys were re-verified, and what turned up — the maintenance record for a library that decays if nobody tends it."
date: 2026-08-26
weight: 5
---

# What Changed

The [about page](/about) says this library is a living map rather than a textbook, and puts numbers on how fast it decays — 70-80% accurate at publication, 50-70% a year later. That claim is only worth anything if somebody is actually tending the map.

This page is that record.

| Published surveys | Re-verified in 30 days | in 90 days | Most recent check |
|---|---|---|---|
| 169 | 28 | 40 | 2026-08-26 |

*Re-verified* means a claim was checked against a primary source — a package registry, a repository, a vendor's own documentation — not that the file was edited. Bulk edits touch every page at once and would make the whole library look freshly checked, which is exactly the kind of number this table exists to avoid.

Entries below say what is true now. They are deliberately not an errata list: a retraction has to restate the thing it retracts, and a claim restated on a page is a claim published on that page — for a reader skimming, and much more so for an agent retrieving. Where a survey changed its mind, the survey itself now simply says the right thing.

## August 2026

*28 surveys re-verified.*

**[1.003 Full-text Search Libraries](/survey/1-003/)**

- lunr.py ranks with BM25, not TF-IDF

**[1.010 Graph Analysis Libraries](/survey/1-010/)**

- The performance gap between NetworkX and igraph is 6x-11x end to end — real, and an order of magnitude smaller than the 40x-250x figures that circulate for this category.
- NetworkX's PageRank is not pure Python — it hands off to SciPy sparse matrices — so the algorithm most often used to demonstrate NetworkX's slowness is the one where it comes closest to the compiled libraries.
- igraph reached 1.0.0 in October 2025 — its first stable major release after fifteen years at 0.x.

**[1.022 Python Optimization Libraries](/survey/1-022/)**

- HiGHS is the default LP engine in both SciPy and MATLAB, and MATLAB has removed its own in-house MILP algorithm in favor of it. SciPy made HiGHS the linprog default in 1.9.0 (2022-07-29); 1.6.0 (2020-12-31) had only added it as an opt-in method. The same 1.9.0 release shipped scipy.optimize.milp, a wrapper around HiGHS, so SciPy's MILP support is HiGHS. MATLAB's linprog default is 'dual-simplex-highs' and 'highs' is the only algorithm intlinprog still has.
- The Mittelmann benchmarks lost their commercial solvers in two waves, not one. CPLEX and XPRESS results were removed in 2018 after IBM and FICO demanded it; Gurobi withdrew in August 2024 and MindOpt followed on 2024-12-24. The benchmark suites themselves are still maintained and current, carrying 2026 run dates.
- GEKKO solves locally by default now, and remote solve was never unique to it. Version 1.3.1 (2025-12-31) flipped GEKKO(remote=...) from True to False because public server load had outgrown the free service, and some solvers and solver options are reachable only with remote=True. Pyomo has long shipped a NEOS/Kestrel interface that submits models to remote servers.
- CVXPY's DCP analysis checks whether an expression is written in a form whose convexity follows from a ruleset — it does not detect convexity. A convex problem can fail the check and be refused at solve time. CVXPY's own tutorial uses sqrt(1 + square(x)), which is convex, is rejected, and is accepted only when rewritten as norm(hstack(1, x), 2).

**[1.062 Python Password Hashing Libraries](/survey/1-062/)**

- passlib has not shipped since 2020-10-08 — nearly six years — while downloads roughly DOUBLED to 41.3M/month
- The OWASP Password Storage Cheat Sheet contradicts itself on bcrypt, and which sentence a reader lands on decides whether they migrate. Its bcrypt section is restrictive; its summary is not.
- bcrypt is actively maintained and still ~3x argon2-cffi's downloads

**[1.075 Deep Learning Frameworks](/survey/1-075/)**

- MXNet serves ~575k downloads/month and does not import
- TorchServe is archived — its README states there will be no planned updates, bug fixes, new features or security patches
- The strongest compatibility guarantee in the category belongs to none of the frameworks
- paperswithcode.com is gone, so every framework adoption share sourced from it is unsupportable

**[1.088 Raster Geospatial Libraries](/survey/1-088/)**

- The official GDAL package on PyPI is still source-only: 3.13.3 (2026-08-18) ships a single sdist and no wheel, as every 3.x release has. What makes `pip install` work for most people is that rasterio's wheels vendor a whole GDAL — now 3.12.4.
- earthpy's installable release is still 0.9.4 from October 2021 on both PyPI and conda-forge, while the repository has tagged three further releases that were never published — v0.10.0 (2025-05-19), v0.10.1 (2025-09-10) and v1.0.0 (2026-08-16).
- The two STAC-to-xarray loaders have diverged further: stackstac's last release and last commit are both 2024-08-10, now two years back, while odc-stac shipped 0.5.3 on 2026-07-30.
- xarray-spatial's revival held: 22 releases reached PyPI in 2026, through 0.10.17 (2026-07-17), with commits continuing to 2026-08-18. But 782 of the 800 commits it has taken since January are by one person, and 1.0.0 has still not shipped.
- rasterio returns plain NumPy arrays and has never had native Dask support; its own concurrency documentation points readers to Dask as an outside tool for images that do not fit in memory.

**[1.091.2 Face Detection & Recognition Libraries](/survey/1-091-2/)**

- InsightFace's AUTO-DOWNLOADED models are non-commercial, while the package is MIT
- dlib's 68-point landmark model cannot be used commercially, though dlib itself is Boost
- The one permissive detection+recognition pair is YuNet (MIT weights) + SFace (Apache-2.0), both in OpenCV core

**[1.115 Form & Validation Libraries](/survey/1-115/)**

- Formik is slow-moving rather than abandoned: 2.4.8 and 2.4.9 shipped in November 2025, including a React 19 ref fix, against 19 million npm downloads a month

**[1.122 Monte Carlo Simulation Libraries](/survey/1-122/)**

- chaospy's predicted collapse has not happened. It has had no commits since 2025-08-29 — close to a full year — yet 4.3.21 installs and runs on Python 3.14 with NumPy 2.5.
- SciPy absorbed quasi-Monte Carlo, but that did not end the standalone design-of-experiments packages. sobol_seq is retired; pyDOE was revived under new maintainers and is now the more active of the two.
- PyMC is built for inference rather than forward simulation — its own README describes it as focused on MCMC and variational inference — but it does ship forward sampling in pymc.draw and pymc.sample_prior_predictive, so calling it unusable for forward Monte Carlo overstates the case.
- SALib has no NumFOCUS backing, despite being the default answer for sensitivity analysis in Python.
- OpenTURNS has the widest copula coverage in this set by a wide margin — more than twenty families — but it is not the only option: chaospy ships Clayton, Gumbel, Joe, Student and Nataf copulas. scipy.stats has none.

**[1.130 Open Source CRM Platforms (Self-Hosted + Managed)](/survey/1-130/)**

- EspoCRM installs on ordinary PHP shared hosting — upload the archive, create a MySQL, MariaDB or PostgreSQL database, run a browser wizard — while its own documentation still tells you to prefer a VPS or dedicated server in production.
- Odoo.sh is not priced per user at all. It bills by worker, storage and staging environment, and its hosting price excludes the Odoo Enterprise license. The optionality sits in Odoo's Custom plan, whose single license covers Odoo Online, Odoo.sh and on-premise.
- All four platforms sell managed hosting, so "self-hosted CRM" names a choice here rather than a requirement.

**[1.148 Morphological Analysis Libraries](/survey/1-148/)**

- Swapping the model package inside one library changes WHICH FEATURE KEYS ARE EMITTED, not the values

**[1.182 Database Diff & Schema Comparison](/survey/1-182/)**

- migra is officially deprecated — its README names 3.0.1663481299 (September 2022) the final release, and points to djrobstep/results as the successor

**[1.205 LLM Evaluation & Testing Frameworks](/survey/1-205/)**

- Ragas has 216 open PRs and zero merged since 2026-03-01, with a dated cause
- DeepEval and Ragas are the same four columns under different names

**[1.304 Procurement & Contracts](/survey/1-304/)**

- Open-source procurement tooling exists and is specific: OCDS Cardinal ships 11 named red flags cited to corruption-risk literature, FollowTheMoney models Contract, ContractAward and CallForTenders directly, and OCDS 1.1.5 is itself the cross-jurisdiction standard with 134 datasets

