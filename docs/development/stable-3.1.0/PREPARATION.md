# ValeLMS 3.1.0 stable preparation

Date: 2026-10-12. Result: **GO for private candidate preparation**, not publication
or final artifact-native acceptance. Base:
`78094377079b73167cc4013d559b9c6101489d48`.

## Supplied independent evidence

Read `.lab/evidence/independent-ux-7809437/REPORT.md` and
`VIDEO-LOCAL-HANDOFF.md` before editing. Their hashes are respectively
`3982b0e7ec31d8fa68bf3c7ed9bfa9b41ceb5b6ae1514d5e6102b5e73dc49281` and
`f0cbb758000165f5f6c7a1b936471822cbd7162cb5999bccc5db39ef78ccb9ec`.
The sanitized [qualification summary](../../qualification-installation-ux.md)
separates real Ubuntu ARM64 testing from earlier WSL2 evidence. It does not
retroactively qualify the final stable archives or authorize access to that VM.

## Exact product correction boundary

1. `plugin/mod_videolessonstream/settings.php`: use supported
   `admin_setting_configempty` for the setup entry instead of a heading.
   Moodle's [New settings filter](https://github.com/moodle/moodle/blob/MOODLE_502_STABLE/public/lib/adminlib.php)
   selects settings whose get_setting() is null. Heading returns true and was
   excluded; the hidden-value setting is initially null, then saves an empty
   normal config value. No wizard/secret/authority or new schema is introduced.
2. `service_setup.php` plus language strings: five clickable guide links using
   Moodle URL/HTML APIs, fixed project HTTPS targets, safe new-tab attributes.
   Existing admin system capability, POST sesskey, protected file and allowlisted
   result rendering remain unchanged. Public main hosts guides; exact candidate
   docs are also bundled. No automatic external request is introduced.
3. `amd/src/upload.js` plus rebuilt `upload.min.js`/map and one language label:
   terminal local transfer outcome gets Failed headline; intentional Pause gets
   paused, Abort aborted. Polling cannot restore Uploading over a terminal local
   failure while the durable session remains resumable. Retry, parts, progress,
   signing, hashing and server authorization mechanisms are unchanged.
4. Plugin `version.php`, `db/upgrade.php`, `classes/local/service_setup.php` and
   component README: 2026101201 / ValeLMS 3.1.0 / STABLE, savepoint only, expected
   service 0.5.0. Numeric version is greater than 2026101200 as requested.
5. Service delta is **only** VERSION, pyproject.toml, README.md and
   deployment/OPERATIONS.md. Runtime Python, schema migrations, dependency lock,
   worker/encoder, storage, grants, quota/recycle/privacy and completion remain
   byte-identical to the accepted baseline. No migration006.

Deployment changes: stable image/installer/readiness identity; optional
VIDEO_API_PORT/VIDEO_GATEWAY_PORT interpolation with loopback fixed; preflight
prestart collision check. Defaults remain 28090/28091; no published MariaDB/Redis.
Documentation includes a concrete second project at 28190/28191, independent
config/tenant/buckets/volumes, and matching trusted HTTPS upstreams.

## Focused validation

- 44 fast Python tests PASS, including version/config/protocol/R2/license
  continuity, actual protected config generation/rerun refusal, alternate Compose
  model and collision/port-bounds tests. No media matrix replay.
- 16 compiled-uploader error/retry/pause/resume/headline cases + 10 existing URL
  security boundaries PASS. New tests assert both message and headline after poll,
  zero committed bytes for failed transfers, and reload recovery without duplicate PUT.
- 127 PHP syntax checks, offline setup/URL/admin/savepoint assertions and six
  stable compatibility cases PASS. XML/SVG and JS syntax checks PASS.
- All 15 AMD modules/maps reproduce exact bytes. PHP 8.3.6, Python 3.12.3,
  Node 18.19.1 in the independent local Linux fast lane; source AMD rebuilt with
  Node 24.17.0. PHPCS unavailable, not claimed as passed.
- Canonical GPL texts, JS bundles, dependency lock, schema and artwork unchanged;
  existing licensing/notice tests and bounded source safety scan PASS. No new
  dependency, storage-server binary or unapproved screenshot bundled.
- Native first-install browser click-through and terminal-fault browser repeat
  are explicitly the next **artifact-native** verification, not claimed from
  offline assertions. The prior dev.3 browser evidence is supplied provenance.

## Packaging and review

One clean local stable-preparation commit precedes both independent builds.
Version-controlled `scripts/public_release.py` builds from exact committed blobs,
normalizes archive metadata, checks safe paths/types and embeds entry inventories.
The two builds must have identical plugin/service bytes and manifests; otherwise
preparation is NO-GO. Old assets are never overwritten. The final source SHA,
sizes, hashes, embedded manifests and reproduction result are generated into the
private packet's RELEASE-MANIFEST.json / SHA256SUMS and local preparation evidence
after this commit, avoiding a self-referential source-commit field.

Packet names: `mod_videolessonstream-3.1.0.zip` and
`valelms-video-service-0.5.0.tar.gz`. Publication, tag and push are not authorized.
The [focused qualification handoff](../../release/stable-3.1.0/QUALIFICATION-HANDOFF.md)
ships with the service package; a companion private handoff records exact hashes.

Existing RC2/dev.3 uses a **coordinated plugin+service upgrade**. Preserve identities,
config, namespaces, storage/media/state, perform normal Moodle savepoint upgrade,
purge caches and Test Connection. No schema006, reseed or retranscode. Native
changed-source adoption still requires an explicit upgrade plan. No hosted action
has occurred. Existing RC1 data migration remains unsupported and documented.

Known limits remain: ordinary-server native installer full media, six-hour/
multi-GiB/full-disk endurance and a new full cross-browser matrix are unqualified;
background watch-credit cause remains unproven. No speculative policy fix.

Evidence under `.lab/evidence/development/stable-3.1.0/`; private final packet
under `.lab/releases/stable-3.1.0/`. Golden LMS mutations, existing LMS connections,
Load Tester VM modifications, production credentials/cloud actions and publication
actions are all **zero**. Next: one focused Deployment artifact verification,
then human-approved stable publication.
