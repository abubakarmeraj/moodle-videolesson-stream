# Changelog

## 3.1.0-rc2 — unreleased qualification candidate

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
  publication review are required; no public RC2 release has been created.

## 3.1.0-rc1 — 2026-10-07 (prepared, not published)

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
