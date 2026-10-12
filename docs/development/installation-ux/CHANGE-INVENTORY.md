# Scoped change inventory

No files removed. Service runtime, migrations, dependency lock, encoder, player,
watch-credit, quota/recycle and media authorization source are unchanged.

## Plugin product changes

- `plugin/mod_videolessonstream/amd/src/upload.js`: categorized sanitized errors,
  separate pause/cancellation, first-error preservation, same bounded retry/resume.
- `plugin/mod_videolessonstream/amd/build/upload.min.js` and
  `plugin/mod_videolessonstream/amd/build/upload.min.js.map`: reproducible generated output.
- `plugin/mod_videolessonstream/lang/en/videolessonstream.php`: upload messages and setup instructions.
- `plugin/mod_videolessonstream/settings.php`: prominent setup link/summary.
- `plugin/mod_videolessonstream/service_setup.php`: five-step onboarding list;
  existing capability, sesskey, protected handoff and allowlisted results retained.
- `plugin/mod_videolessonstream/version.php`: unreleased dev.3 / 2026101200 / ALPHA.
- `plugin/mod_videolessonstream/db/upgrade.php`: idempotent savepoint only, no DDL/data mutation.
- `plugin/mod_videolessonstream/README.md`: accurate unreleased identity.

## Installation / checks

- Added `deploy/setup.py`: guided protected generation, existing preparer invocation.
- Added `deploy/preflight.py`: local default, explicit online/authenticated checks
  and opt-in own-key synthetic storage probe.
- Added `deploy/installer/policy.py`: shared HTTPS/role-file/policy validation.
- `deploy/docker/prepare.py`: shared validation, symlink refusal, safe invalid-policy error.
- `deploy/docker/compose.yaml`: six raw env-file entries; no architecture/resource/routing change.
- `scripts/check_release.py`: new uploader/onboarding tests and phase-specific local evidence path.
- `scripts/public_release.py`: current dev identity/manifests, reject unauthorized
  development release builds, verify historic plugin identity against its own embedded manifest.
- `tests/test_release.py`: development identity expectations; service stays RC2.
- `tests/test_upload_urls.cjs`: reusable compiled-module harness, richer test doubles,
  optional local baseline AMD input; existing ten security cases retained.
- Added `tests/test_upload_errors.cjs`: fourteen error/retry/pause/resume cases.
- Added `tests/test_installation_ux.py`: eleven offline/config/preflight tests.
- Added `tests/test_installation_guidance.php`: offline guidance/savepoint/admin guards.
- Added `tests/check_installation_storage.py`: explicitly opt-in new disposable
  HTTPS MinIO role/probe integration; excluded from automatic unit discovery.

## Documentation / inventory

- `README.md`, `CHANGELOG.md`, `docs/development/README.md`: current front door/history/router.
- `docs/quick-start.md`, `docs/docker.md`, `docs/native-linux.md`,
  `docs/installation.md`, `docs/storage.md`, `docs/troubleshooting.md`,
  `docs/known-limitations.md`: clearer installation, corrected protocol tuple,
  accurate qualification boundaries and storage diagnostics.
- Added `AGENTS.md`, `docs/ai-installation.md`, `docs/preflight.md`,
  `docs/installation-examples.md`, `docs/qualification-ubuntu-arm64.md`.
- Added this run's `docs/development/installation-ux/RESULTS.md`, `HANDOFF.md`,
  `watch-progress-plan.md`, and `CHANGE-INVENTORY.md`.
- `.gitignore`: expose only this new public development-report folder, not local evidence/secrets.
- `docs/release/IDENTITY.json`, `PRODUCT-MANIFEST.json`,
  `PUBLIC-SOURCE-MANIFEST.json`: current development fingerprints. Service manifest
  remains byte-identical. Frozen tagged RC1/RC2 sources/assets remain unchanged.

Local generated test/evidence files under ignored `.lab/` are not product or
publication content. Machine-readable exact path/hash inventory is in
`.lab/evidence/development/installation-ux/CHANGE-INVENTORY.json`.
