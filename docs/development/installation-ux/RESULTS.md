# Installation-experience implementation and focused qualification

Date: 2026-10-12. Result: **PASS for scoped local development; not a release approval**.

Branch: `codex/installation-experience`, starting at
`f1cbf624250bc4c64f057f3fddcac4f03ae7e2c1`.
Plugin: **mod_videolessonstream 2026101200 / ValeLMS 3.1.0-dev.3**, unreleased.
Service runtime: **0.5.0-rc2**, protocol **2**, migrations **001–005**, unchanged.
Plugin upgrade is an idempotent savepoint only; no schema or data changes.

## What changed

- Upload cancellation and intentional pause are separate. First terminal part
  error survives sibling cancellation and polling. Storage HTTP failure, temporary
  connection/timeout, authorization expired **or denied**, service request failure,
  missing CORS ETag and intentional pause have sanitized messages. Parts retry
  with fresh authorization; committed-part resume identity remains intact.
- Guided protected configuration calls the existing manifest-guarded preparer,
  uses hidden key prompts, refuses existing directories/symlinks and validates
  HTTPS origins, distinct buckets, host allowlist and protected role key files.
- Preflight is read-only by default. Explicit online mode checks DNS/trust/health
  and signed compatibility/readiness; explicit storage probe tests actual writes,
  not just HEAD, and cleans only its own tiny random keys/uploads.
- Compose raw env-file handling preserves literal credential characters.
  Regression first proved ordinary interpolation removed a synthetic `$` value.
  Development tooling requires Compose >= 2.30; older releases are not changed.
- Moodle settings link prominently to Video Service configuration and five clear
  setup steps, preserving system capability and POST sesskey checks. Protected
  connection-file contents/credentials remain undisplayed.
- Public guides now explain the two-piece installation, build-before-start,
  current RC2/protocol-2 tuple, generic S3/role/CORS/HTTPS proxy and SeaweedFS
  examples. The AI guide refines the tester's proposal but uses the same human
  process, tools and safety boundaries. AGENTS.md is a concise router.
- Separate supplied Ubuntu ARM64/SeaweedFS evidence is documented without private
  host identifiers. The background-watch observation has a controlled plan only;
  watch-credit/completion code is unchanged.

## Tests and evidence

| Check | Result / limit |
|---|---|
| RC2 compiled uploader negative test | FAIL as expected: HTTP 500 → cfuploadpaused, not cfuploadstorage |
| Patched compiled uploader | 14 error/recovery/pause/resume scenarios PASS |
| Existing upload URL boundaries | 10 scenarios PASS, including generic S3/R2, HTTPS and authenticated plan |
| Installer/preflight contracts | 11 tests PASS on root Linux; actual config generation/rerun refusal, private modes, symlinks, Compose parsing, signed readiness/failures, offline no-network/no-write, disk vs RAM staging |
| Full fast Python set | 43 tests PASS, including existing R2/protocol/identity/security contracts |
| PHP | 127 files linted; 6 compatibility cases and onboarding/savepoint assertions PASS |
| JS / AMD | 36 files syntax-checked; all 15 AMD modules/maps reproduced byte-for-byte |
| XML/SVG | 3 XML / 3 SVG parsed and existing SVG safety checks PASS |
| New disposable local MinIO | Distinct role credentials, verified test TLS, presigned PUT/OPTIONS/ETag, multipart/list/complete/abort, HEAD/read/range/write/delete PASS |
| Storage negative/cleanup | Gateway raw access denied; default trust rejects test certificate; zero probe objects/incomplete uploads left; test container removed |
| Public-source safety scan | Bounded path/private-marker/credential-signature checks PASS; not a universal secret detector |
| Native Moodle onboarding UI | PHP syntax/offline contracts only; new browser render not claimed |
| Fresh ordinary-host timed installation | Not rerun; no invented elapsed speedup |
| Broad media/browser/endurance qualification | Intentionally not repeated |

Tests used the independent local Linux environment, PHP 8.3.6, Python 3.12.3,
Node 18.19.1 for fast Linux checks; AMD also rebuilt/tested with Node 24.17.0 on
the workstation. PHPCS was unavailable; no PHPCS PASS is claimed. Existing
service/runtime/container resources were not reconfigured; only a new disposable
storage probe container was created and removed. No Moodle site was contacted.

Ignored evidence under `.lab/evidence/development/installation-ux/`:
`FAST-REGRESSIONS.json`, `FOCUSED-EVIDENCE.json`, `STORAGE-PROBE.json`,
`CHANGE-INVENTORY.json`, `FINAL-BOUNDARIES.json`.

## Improvement measurement without overstating it

Guided generation is verified to accept **7 configuration answers + 8 hidden role
key entries**, then generate **9 policy/key files + 12 runtime files**. No manual
JSON/env editing is required on this default path; one setup command replaces the
ValeLMS policy/key-file authoring step and invokes preparation. Storage account/
IAM/CORS, DNS/TLS and proxy provisioning remain explicit operator prerequisites.
Advanced region/addressing/CA uses an existing protected policy.

The supplied real-VM run took 40m36s overall / 20m23s to first play, with 33 shell
submissions and 15 authored files (including unused/diagnostic files). Those are
different scopes from configuration generation; **no 15→0 total-file or elapsed
speedup claim** is made. A comparable timed successor install is pending.

## Provenance and immutability

The independent report SHA-256 is
`4e9248e56a5e0c39c8e3e50d22028460508f5f91c8a15851a9e4ba72d809985a`.
Private paths/hostnames, secret retrieval material and raw screenshots were not
copied into public source. Service source manifest remains
`deebb636977118d3ac8dbf2c7ced697703db2fa7bffcce59c3dae5d7ca788620`.
The current development product index is recorded in docs/release/IDENTITY.json;
it is intentionally **not** the qualified RC2 product index.

RC1 tag still points to `3c2f59f704421f199033f020fd60eec50ea84a8d`;
RC2 tag still points to `57862457cabba6d5c305f543a9d0f4e66fb60ded`.
Existing RC2 plugin/service files still hash to
`2792f1e99c56ea1a5458cb16f12742b447042c9ba52dc80265c7fa1d243b8600` /
`47135d42d6f87565253b76a32f1c8bf835810493678d4d197a709e3713dbf61a`.
No new artifact/tag, remote push or publication. Golden LMS, Load Tester VM,
existing LMS, production credentials and production/cloud resources: **0 actions**.

## Remaining boundaries

No implementation blocker found. Before a successor release, review this branch,
qualify the changed Moodle guidance/error messages in a native browser workflow,
and run a narrowly scoped timed fresh Ubuntu installation using these tools.
Deployment still owns storage IAM/CORS/TLS, proxy, backups and adequate real
disk-backed staging. Preflight cannot certify a remote browser/PHP host or
endurance, nor guarantee capacity against unrelated disk consumers. See
[handoff](HANDOFF.md). No new storage backend or watch-credit patch was introduced.
