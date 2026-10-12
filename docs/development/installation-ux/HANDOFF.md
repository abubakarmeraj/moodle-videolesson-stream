# Installation-experience review handoff

This is **unreleased development**, not authority to deploy/publish. See
[results and exact limits](RESULTS.md). No new release assets were built.

## Resulting source / compatibility

- Branch `codex/installation-experience`; base
  `f1cbf624250bc4c64f057f3fddcac4f03ae7e2c1`.
- Plugin 2026101200 / ValeLMS 3.1.0-dev.3, component mod_videolessonstream.
  Savepoint only from published RC2; no table/column/data migration.
- Service runtime stays exact 0.5.0-rc2, protocol 2, migrations 001–005.
  No new service migration. Deployment tooling/docs changed separately.
- Reviewed source hashes: docs/release/PRODUCT-MANIFEST.json,
  SERVICE-MANIFEST.json, PUBLIC-SOURCE-MANIFEST.json and IDENTITY.json.
  The unreleased build guard prevents accidental RC2 artifact reuse.
- Public RC1/RC2 tags/archives remain immutable. No branch push/publication.

## Administrator journey after review / successor packaging

1. Install the matched future plugin ZIP normally; follow its setup heading/link.
2. Provision private S3 raw/processed buckets, role credentials, exact-origin CORS,
   trusted HTTPS/DNS and private disk staging. See [examples](../../installation-examples.md).
3. Run `sudo python3 deploy/setup.py --directory /etc/valelms-video` once, with
   hidden keys. Existing policy is supported via `--config`; reuse installed
   runtime identity, never regenerate it to recover a startup failure.
4. Run local [preflight](../../preflight.md); build the shared local service image,
   then start Compose with the storage-network overlay. Development tooling
   requires Compose >= 2.30 for literal credential preservation.
5. Configure the reviewed HTTPS proxy; run `--online --handoff ... --storage-probe`
   from the locked service/operator Python environment. FAIL needs remediation;
   PENDING never means verified. The probe only owns tiny random synthetic keys.
6. Securely install the six-field JSON outside Moodle webroot, root:PHP group
   0640/parent 0750. Save only its local path in Video Service configuration.
7. Test Connection: compatible 0.5.0-rc2/protocol 2, schema 001–005, both buckets,
   Redis and fresh worker capacity. Teacher native short upload → Ready; enrolled
   student playback and persisted progress/completion. This remains mandatory.

## Narrow reviewer/next-tester checklist

- Inspect upload messages in a native browser: intentional pause vs storage 500,
  authorization 403, transient network, server error and missing exposed ETag.
  Ensure no URLs/provider text leak, no poll overwrite, committed-part resume works.
- Confirm setup instructions/link and protected path are usable to a Moodle
  administrator; student/teacher do not gain configuration capability.
- Fresh ordinary Ubuntu ARM64/amd64 install, same tool path as humans; measure
  start/end, submissions, manually edited files and decisions. Do not copy the
  earlier tester's elapsed numbers onto the new tools.
- Existing-state rerun must refuse regeneration and preserve tenant/subject key.
  Keep DB/media and matched recovery intact; no routine down -v/drop/delete.
- Do not assume MinIO download availability. SeaweedFS 4.48 is a separately
  verified example, not bundled or automatically provisioned.
- Background watch-credit observation goes to its [controlled plan](watch-progress-plan.md),
  not a speculative completion-policy fix.

Fast checks: `python -B scripts/check_release.py` in a prepared locked environment.
Optional local storage probe integration: `python -B tests/check_installation_storage.py`
(existing cached test images, new disposable storage only; no LMS/media matrix).
No real-host browser result or full fresh-host successor qualification is claimed.
