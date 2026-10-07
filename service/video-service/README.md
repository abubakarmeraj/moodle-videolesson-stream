# ValeLMS Video Service 0.5.0-rc2

Separate media processing/delivery service for Video Lesson3.1.0-rc2.
Protocol2; MariaDB migrations001–005. Project-owned source is GPL-3.0-or-later;
third-party libraries retain their own licenses. LICENSE and notices are supplied.

Roles: signed API, authorized gateway, durable dispatcher, leased FFmpeg worker,
janitor and explicit migrator. MariaDB owns lifecycle/accounting; Redis supplies
transport/replay/rate/capacity coordination. Storage supports private R2 and generic
S3-compatible endpoints. Local filesystem storage is absent. MinIO is not bundled.

Use the extracted distribution's docs/docker.md (recommended) or docs/native-linux.md.
The standalone Dockerfile starts only the API; it is not the complete role stack.
Protected role configuration and trusted HTTPS are required. Dependency health
alone does not prove storage/CORS/media readiness. Use Moodle Test Connection and
one short upload/playback smoke. See docs/known-limitations.md and deployment/OPERATIONS.md.

New clients sign `/v2/rpc` with X-VL-Key/Time/Nonce/Signature. Temporary authenticated
protocol1 aliases can be disabled with SERVICE_ALLOW_LEGACY_PROTOCOL=false; they
are not a Moodle component/data migration. Preserve existing explicit Redis
namespaces and independent tenant/reference authorities during controlled upgrades.
