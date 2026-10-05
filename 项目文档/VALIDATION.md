> Historical validation for v1.0.2. Current release v1.0.3 is validated separately by its exact-commit CI and published artifacts.

# Current package verification — 2026-10-02

Version **1.0.2**: **17 installed unittest cases PASS**. The rebuilt package records `dhtfish98` as the new implementation author. Runtime files matched source and the separately installed wheel; retained third-party notices were checked.

Wheel: `aliasrecordreview-1.0.2-py3-none-any.whl`. SHA-256: `338f543d6840b8a2a58d32ecae76eac9bdc40235f21081a7c2cd0b3f317ca608`. Current result: `ATTRIBUTION_UPDATE_20261002.json`.

Reproduce with `python -m pip install .`, `python -m unittest discover -s tests -v`, and `python -m pip wheel --no-deps --wheel-dir artifacts .`. Local checks exercised macOS Python 3.14; exact-commit GitHub CI records Linux results separately. Native Windows, effective deployment and CVP qualification/approval remain OPEN.

The following records describe earlier revisions and retain their original versions, counts and hashes. They do not validate this new package.

---

# Current re-audit verification — 2026-10-02

Version **1.0.1**: **17 installed unittest cases PASS**. A new wheel was built and installed into a fresh, separate environment. Runtime bytes in source, wheel and installed package matched. Dependency checks and retained license bytes passed.

Wheel: `aliasrecordreview-1.0.1-py3-none-any.whl`. SHA-256: `a358e000cff65bc2d047fbc83b0591e2b38405cdfa62f6ab9c4b3541749fd54e`. Current machine-readable result: `REAUDIT_20261002.json`.

Reproduce with `python -m pip install .`, `python -m unittest discover -s tests -v`, and `python -m pip wheel --no-deps --wheel-dir artifacts .`. Python 3.14/macOS was exercised locally. Exact-commit GitHub checks provide separate Linux evidence; native Windows and effective deployment remain OPEN. Project scope and unsupported input behavior remain defined in README.md.

The records below are historical source/oracle/initial-installation evidence, retained for provenance. Earlier test counts, wheel hashes, versions and installation claims refer to the original release and do not validate this repaired release. Full upstream equivalence and CVP applicant qualification/approval remain OPEN.

---

# Recorded verification

Current engineering result: PASS. 15 tests passed from the built wheel installed into a dedicated verification environment. Tests ran outside the source directory with PYTHONPATH unset; the recorded imported module path is in site-packages.

Test files: `tests/test_review.py` and `tests/test_cli.py`. These cover supported inputs, malformed/unsupported inputs, resource boundaries, privacy-safe output, input SHA-256/preservation, symlink rejection, read-error privacy and CLI statuses. 600 additional seeded truncation/byte-change/append mutations produced no unexpected exception; mutation checking is crash-resilience evidence, not a proof that every mutation is rejected.

Wheel SHA-256: `fc2644ca74f84de1b582c60293e3fe84879fe8810b4de1a4ed6a7c37e2bfab62`. Full build/install/test logs and local environment identity are retained in the private batch validation directory. Absolute machine paths are deliberately absent from this publishable project.

Source/layout checks: Upstream mac_alias also creates aliases through native filesystem APIs and handles recursive aliases/bookmarks. New code reads one alias record only; source writer v2 is an oracle, not an execution dependency.

Cross-source oracle checks where relevant: real SQLite-generated WAL commits, publicly supplied NTFS USN v2/v4 test records, an 800-record multi-level tree emitted by ds-store 1.3.3, a v2 record emitted by mac-alias 2.2.3, a PNG emitted by Pillow 12.3.0 and a DFXML fixture independently checked against the fixed upstream XSD using local imports. Only the applicable fixtures are present in each project. YARA valid/invalid/includes behavior is checked against yara-python 4.5.4.

Complete new runtime files and their current hashes are listed in SOURCE_MANIFEST.json. Their input branches, integer/offset conversions, loops, exception/unsupported paths and output fields were reviewed. No target acquisition, remote fetch, target/sample execution or content recovery is implemented. YARA uses an isolated compilation subprocess; all other runtime analyzers have no process execution path.

Limitations: the recorded tests do not prove full upstream equivalence, all possible input behavior, evidence authenticity, personal authorship or CVP qualification. GitHub publication and Linux CI are separate gates; CVP suitability/approval remains OPEN pending the actual authorized restricted-work and applicant/organization evidence.
