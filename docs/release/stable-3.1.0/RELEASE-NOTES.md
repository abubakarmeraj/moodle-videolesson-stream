# ValeLMS Video Lesson Stream 3.1.0 — prepared stable candidate

Plugin **2026101201 / ValeLMS 3.1.0**, service **0.5.0**, protocol **2**,
schema migrations **001–005**. Packages remain private pending final focused
artifact-native verification and human-approved publication. No tag/push/release
publication is authorized in this preparation phase.

ValeLMS adds private adaptive video lessons with direct multipart/resumable
uploads, FFmpeg no-upscale processing, authorized HLS playback, Moodle-owned
watch progress/completion, reusable references, quota and recycle/recovery.

Changes since the accepted installation-UX baseline:

- Setup link now appears as a supported hidden-value setting in Moodle's
  first-install New settings screen, not only the normal plugin settings page.
- Five-step administrator onboarding includes clickable human installation,
  storage, connection, troubleshooting and first-video guides.
- Terminal browser upload failure shows Status: Failed. Automatic retries,
  intentional pause/resume, reload recovery, durable progress and sanitized
  causal messages are preserved.
- Alternate loopback API/gateway port variables and opt-in prestart collision
  checks support separate Compose projects on one host, without publishing DB/Redis.
- Stable plugin/service compatibility metadata aligned; service runtime logic,
  lock, protocol, migrations, encoder/player/storage/security remain unchanged.

Moodle upgrade is savepoint-only from RC2/dev.3, no new schema/data migration.
Service 0.5.0 retains migrations 001–005, no006. Upgrade the **coordinated pair**;
plugin-only replacement leaves an old service incompatible. Preserve installed
tenant/subject/configuration and existing media; no reseed/retranscode needed.
See [upgrading](../../upgrading.md) and [limits](../../known-limitations.md).

Supported core functionality does not certify arbitrary Linux/S3 providers or
large endurance workloads. Existing RC1 uses a distinct Moodle component; automatic
RC1 activity migration is not supplied. RC1/RC2 history/assets remain immutable.

Project-owned code/artwork is GPL-3.0-or-later. Canonical LICENSE, inherited
copyrights, bundled JS grants, Python notices and dependency lock remain intact.
No new dependency, binary storage server, container image or unapproved screenshot
is bundled. See THIRD_PARTY_NOTICES.md in the distribution.

Authoritative candidate hashes/source commit are in the companion outer
RELEASE-MANIFEST.json and SHA256SUMS, generated from the clean committed source;
embedded RELEASE-MANIFEST.json inventories every component archive entry.
