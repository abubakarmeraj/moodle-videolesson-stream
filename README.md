# ValeLMS Video Lesson Stream

Add private, adaptive video lessons to Moodle. Teachers upload a video; students
watch it inside their course with saved progress and completion. Your own Linux
Video Service processes the upload—no ValeLMS-hosted subscription is required.

You install **two pieces**: a normal Moodle plugin ZIP and a separate Video
Service. You also need private S3-compatible storage and trusted HTTPS. The ZIP
alone cannot encode or host videos. [Start the installation here](docs/quick-start.md).

## Features

- Private direct multipart/resumable uploads, independent upload limits and tenant quota.
- FFmpeg HLS processing, no-upscale administrator-owned renditions, 4-second default segments.
- Adaptive/manual quality, speed controls and renewable playback authorization.
- Moodle-controlled access, watch progress and completion; safe reusable references.
- Durable processing status, recycle/recovery and retention cleanup.
- Guided protected setup, preflight storage write checks and Moodle Test Connection.

**Recommended release: [ValeLMS 3.1.0 Stable](https://github.com/abubakarmeraj/moodle-videolesson-stream/releases/tag/v3.1.0)** —
plugin **2026101201 / ValeLMS 3.1.0**, Video Service **0.5.0**, protocol **2**.
The exact packages passed [final artifact-native qualification](docs/qualification-stable-3.1.0.md)
and were approved for publication. Core functionality is supported within the
[documented environment/qualification limits](docs/known-limitations.md), not a
certification of every Linux distribution, S3 provider or workload.

## Quick start

Download the matched plugin ZIP, service archive and checksums from the
[Stable release](https://github.com/abubakarmeraj/moodle-videolesson-stream/releases/tag/v3.1.0).

1. Install the verified `mod_videolessonstream-3.1.0.zip` through Moodle's plugin installer.
2. Install the separate Video Service using [Docker Compose](docs/docker.md),
   with private S3-compatible storage and trusted HTTPS endpoints.
3. Place the generated protected connection handoff on the Moodle server and
   configure its server-local path under **Site administration → Plugins →
   Activity modules → Video Service configuration**.
4. Click **Test Connection**. Require compatible service, storage, Redis and worker readiness.
5. Add **ValeLMS Video Lesson Stream**, save and display, then upload a short test video.

The Moodle ZIP **does not install Linux services**. The Video Service is required,
on the same server or another server. Compose is the recommended installation
path; [native/systemd](docs/native-linux.md) is an advanced clean-host option.
Storage accounts/buckets, DNS and HTTPS are operator prerequisites, not automatically provisioned.

See the [short quick start](docs/quick-start.md), [requirements](docs/installation.md),
[configuration](docs/configuration.md), [storage contract](docs/storage.md),
[upgrading](docs/upgrading.md), and [known qualification limits](docs/known-limitations.md).
Cloudflare R2 and generic S3-compatible storage are supported. MinIO (WSL2) and
SeaweedFS 4.48 (ARM64 VM) were used for separate qualification runs, not bundled.
Local-filesystem storage is not implemented. [AI installation agents start here](docs/ai-installation.md).

## Existing installations

The Moodle component is **`mod_videolessonstream`**, installed under
`mod/videolessonstream`. Existing prerelease users must read [upgrading](docs/upgrading.md).
RC1 used a different component: [the RC1 identity/data boundary](docs/rc1-to-rc2.md)
is not an automatic migration. Published RC1/RC2 tags and assets remain immutable.

## Storage

**Cloudflare R2 — first-class supported backend:** dedicated R2 configuration,
private raw/processed buckets, direct browser multipart upload with short-lived
signed parts, and private processed HLS media. No public bucket is required.

**Generic S3-compatible storage — supported:** MinIO was used for independent
qualification; compatibility varies by provider. R2's dedicated compatibility
regressions are separate from live disposable-cloud qualification. See
[storage setup, TLS, CORS and permissions](docs/storage.md).

## Project

`plugin/mod_videolessonstream/` is the Moodle component; `service/video-service/` is the
separate service. `deploy/` supplies Compose/native tooling; `tests/` and `scripts/`
are developer checks. See [architecture](docs/architecture.md),
[contributing](CONTRIBUTING.md), [security](SECURITY.md) and [changelog](CHANGELOG.md).

Project-owned code is **GPL-3.0-or-later**; original ValeLMS artwork uses the
same license. Upstream copyrights and dependency licenses remain intact. See
[LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) for development,
tests, focused pull requests and DCO/Signed-off-by guidance. Follow our
[Code of Conduct](CODE_OF_CONDUCT.md).

## Issues

[Bugs, feature requests and installation questions](https://github.com/abubakarmeraj/moodle-videolesson-stream/issues/new/choose)
are welcome. Use the templates and share only sanitized information.

## Security

Read [SECURITY.md](SECURITY.md) for the current private reporting contact.
**Do not report vulnerabilities through public Issues, Discussions or PRs.**

## License

Project-owned code and original artwork are **GPL-3.0-or-later**. See
[LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
Third-party code and community-policy material retain their respective terms.
