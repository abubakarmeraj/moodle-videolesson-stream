# ValeLMS Video Lesson Stream

> RC2 is a release candidate, not stable software or an in-place RC1 upgrade.
> Its exact distributions passed focused installation and media qualification
> on Ubuntu 24.04 WSL2, then an independent Ubuntu 24.04.5 ARM64 VM installation
> with Moodle 5.2.4 and SeaweedFS. See the [RC2 release](https://github.com/abubakarmeraj/moodle-videolesson-stream/releases/tag/v3.1.0-rc2)
> for verified assets, qualification scope and known limits. RC1 remains immutable.

Add private, adaptive video lessons to Moodle. Teachers upload a video; students
watch it inside their course with saved progress and completion. Your own Linux
Video Service processes the upload—no ValeLMS-hosted subscription is required.

You install **two pieces**: a normal Moodle plugin ZIP and a separate Video
Service. You also need private S3-compatible storage and trusted HTTPS. The ZIP
alone cannot encode or host videos. [Start the installation here](docs/quick-start.md).

Distinct Moodle activity: **`mod_videolessonstream`**, installed under
`mod/videolessonstream`. It is not the original `mod_videolesson` plugin.
RC1 users: read the [breaking identity transition](docs/rc1-to-rc2.md) first;
RC2 does not automatically upgrade or migrate RC1 activities.

**Release candidate:** plugin **3.1.0-rc2** (2026100702), Video Service
**0.5.0-rc2**. This is not a stable release. No ValeLMS-hosted account is needed.

This development branch contains unreleased **3.1.0-dev.3** (2026101200)
installation improvements. Service runtime remains **0.5.0-rc2** / protocol 2.
New setup/preflight commands below are development source, not retroactively
included in the immutable RC2 download. Do not mix development and release files
on a live installation; await a reviewed successor distribution.

## Quick start

1. Install `mod_videolessonstream-3.1.0-rc2.zip` through Moodle's plugin installer.
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

## Features

- Private direct multipart/resumable uploads, independent upload limits and tenant quota.
- FFmpeg HLS processing, no-upscale administrator-owned rendition policy, 4-second default segments.
- Bundled player libraries, adaptive/manual quality, speed controls and renewable authorization.
- Moodle-owned access, watch progress and completion; safe reusable references and relinking.
- Durable processing status, recycle/recovery and retention cleanup.
- Signed service setup/readiness checks, role-separated worker/dispatcher/gateway/janitor.

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
