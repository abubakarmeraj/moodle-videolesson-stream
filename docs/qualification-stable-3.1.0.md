# ValeLMS 3.1.0 Stable — final qualification scope

The exact **mod_videolessonstream 2026101201 / ValeLMS 3.1.0** and **Video Service
0.5.0** distributions passed final artifact-native Deployment qualification:
**PASS_FOR_STABLE_PUBLICATION_APPROVAL**. The human owner subsequently explicitly
approved Stable publication. Source tag `v3.1.0` identifies qualified commit
`edd85c8be803a9c6776c3d55efa121839957e60e`.

| Qualified asset | SHA-256 |
|---|---|
| mod_videolessonstream-3.1.0.zip | 08e7c27ffffa95ee7db19150a10bfec7679e0a7c31cd0394db83338107840886 |
| valelms-video-service-0.5.0.tar.gz | 0e7550f25e55bc6e4e0cb7ea5c8ec23eebe5692301a34c8637c8865038d6f1a7 |

Archives were not patched or rebuilt for publication. Their embedded inventories,
preparation-stage wording and source identity are preserved as historical
provenance. Current public main can contain later documentation-only publication
updates; it is not a reason to move the release tag or regenerate its archives.

## Final environment and checks

Ubuntu **24.04.5 WSL2**, real systemd, PHP **8.3.6**, MariaDB, packaged Python
service/FFmpeg **5.1.9**, trusted lab HTTPS and private generic S3-compatible
storage. Fresh Moodle **5.2.4 (Build 20261005)** and a separate isolated
**5.2.2** RC2-to-Stable upgrade clone were exercised. Moodle core stayed unchanged.

- Exact archive/source manifests, safe paths/types, licenses/notices and bounded
  private-content/secret scans passed. Installed runtime files matched packages.
- Native Moodle ZIP installation and actual **New settings** setup entry passed;
  all five documentation links were clicked with safe new-tab attributes.
- Protected administrator setup/Test Connection passed; teacher/student access
  to service configuration was denied.
- Terminal storage HTTP500 and hidden ETag showed **Status: Failed** plus useful
  sanitized messages after polling. Transient retry and intentional Pause/reload/
  same-file resume passed; committed part 1 was skipped on resume.
- Private HTTPS multipart upload, FFmpeg/HLS, decoded student playback/seeking,
  natural watch and persisted completion passed. Accepted synthetic video was
  about 18 seconds / 20 MB, not an endurance or large-file benchmark.
- Activity deletion, recycle without freeing physical bytes, keep, native restore,
  authorized relink and recovered playback/completion passed. This does not claim
  that Moodle backup contains physical media.
- Independent Compose stacks, alternate loopback ports, collision negatives and
  restart persistence passed; database/Redis had no published ports.
- Coordinated RC2-to-Stable upgrade passed. Plugin/reference/progress/completion
  and representative service/media/accounting records were preserved. Old RC2
  service was rejected by the Stable plugin until the matched upgrade completed.
  Migrations remain **001–005**, no006, with no pending Moodle upgrade.

## Limits retained

This final run is **WSL2**, not a new ordinary Ubuntu/ARM64 server certification.
The earlier independent [Ubuntu ARM64 installation](qualification-ubuntu-arm64.md)
and [installation-UX verification](qualification-installation-ux.md) are separate
baseline evidence. No fresh live-R2 account test, six-hour/multi-GiB/full-disk
endurance or full new Firefox/WebKit matrix is claimed. The background watch-credit
observation remains unproven; no completion policy was weakened. RC1 activity
migration remains unsupported; RC2-to-Stable is the supported same-component path.

Detailed environment/recovery records remain private. No Golden LMS or hosted
deployment was needed for qualification or publication. Download only the
[matched Stable assets](https://github.com/abubakarmeraj/moodle-videolesson-stream/releases/tag/v3.1.0)
and verify SHA256SUMS. See [known limits](known-limitations.md), [Quick Start](quick-start.md)
and [AI-assisted installation](ai-installation.md).
