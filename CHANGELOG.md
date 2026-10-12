# Changelog

## 3.1.0 — stable candidate, not yet published

Plugin 2026101201 / ValeLMS 3.1.0; Video Service 0.5.0; protocol 2,
migrations 001–005. Private artifact verification and human publication approval
are still required. RC1/RC2 tags and published assets remain immutable.

- First-install Moodle New settings now includes the setup entry, with clickable
  guide links on the protected five-step page.
- Terminal upload failures show Status: Failed; pause/retry/resume and sanitized
  causal messages are preserved, including during status polling.
- Independent Compose stacks support explicit alternate loopback ports, with
  prestart collision checks and a complete two-stack/proxy example.
- Clearer stable front door and matched human/AI instructions; independent
  Ubuntu ARM64 UX qualification is recorded separately from WSL2 evidence.
- Savepoint only, no new Moodle schema or service migration006. No encoder,
  player, storage, authorization, quota/recycle or completion-policy redesign.

## 3.1.0-dev.3 — unreleased installation experience

- Distinguish upload pause from storage, transport, authorization and service
  request failures; preserve multipart resume and sanitize all displayed errors.
- Guided protected Compose policy generation and opt-in preflight/write probes;
  clearer Moodle onboarding, proxy/storage examples and human/AI install guides.
- Record separate real Ubuntu ARM64/SeaweedFS RC2 evidence and an unproven
  background watch-credit observation. No watch-policy or service runtime change.
- Plugin savepoint 2026101200 only; no schema/data migration. Published releases
  and assets remain immutable; no new release is authorized here.

## 3.1.0-rc2 — published prerelease

- Owner-approved distinct Moodle activity `mod_videolessonstream` (2026100702),
  ValeLMS Video Lesson Stream. Moodle names cannot contain an internal underscore;
  the original requested spelling was rejected and is not shipped.
- Isolated component-owned tables, capabilities, config, files, callbacks,
  scheduled tasks, backup/restore, templates and rebuilt AMD modules.
- ValeLMS Video Service0.5.0-rc2 with neutral authenticated protocol2; temporary
  explicit protocol1 aliases retain HMAC and replay protection.
- First-class R2 documentation and dedicated synthetic client regressions;
  generic S3/MinIO remains supported. No new live-cloud qualification claimed.
- This is not an automatic RC1 data migration. RC1 remains immutable; see
  [transition guidance](docs/rc1-to-rc2.md). Deployment qualification and separate
  publication review were completed for the immutable RC2 distributions.

## 3.1.0-rc1 — 2026-10-07 (published prerelease)

Coordinated with Video Service0.5.0-rc1, protocol1, migrations001–005.

- Moodle Video Lesson activity with private direct multipart/resumable browser upload.
- Operator-owned generic S3-compatible storage and Cloudflare R2 support.
- FFmpeg HLS processing, administrator-owned no-upscale renditions and segment policy.
- Authorized adaptive/manual playback with speed controls and renewable grants.
- Moodle-controlled progress/completion, reusable references and safe relinking.
- Durable status, quota accounting, recycle/recovery and bounded retention cleanup.
- Protected service setup/Test Connection, Docker Compose and native/systemd paths.
- Original CodeFortex geometric activity/placeholder artwork and GPL-3.0-or-later
  project-code licensing; third-party grants/notices retained.

RC1 is not stable. See known-limitations.md for the exact qualification boundary.
