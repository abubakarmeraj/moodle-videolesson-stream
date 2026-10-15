# Security

## Private reporting

Report suspected security vulnerabilities privately to
[abubakar.meraj11@gmail.com](mailto:abubakar.meraj11@gmail.com).
This is the owner-approved temporary contact.
**Do not report vulnerabilities through public GitHub Issues, Discussions or PRs.**
Do not post exploit details, credentials or customer data publicly.

Include affected versions, impact and reproducible steps, removing signing keys,
passwords, credentials, cookies, presigned URLs and private media. If sensitive
details are essential, first arrange a suitable private channel with the maintainer.
Investigation/disclosure will be coordinated; no response-time guarantee is offered.

## Supported line

The supported Stable pair is ValeLMS 3.1.0/plugin plus 0.5.0/service, protocol 2.
Use the matched assets from the v3.1.0 release. No maintenance window is guaranteed.

## Model

Moodle authorizes users/activity access and completion. Signed RPC, replay bounds,
short-lived exact-object/part upload authorization and renewable media grants
bind the service to current Moodle authority. Buckets remain private. Teacher
inputs do not choose storage endpoints, permanent credentials or encoding policy.

Keep API/gateway behind trusted HTTPS, DB/Redis off public networks, roles and
secrets scoped, TLS verification enabled and worker staging private. Never publish
connection handoffs, secret keys, cookies, full presigned URLs or raw RPC bodies.
Use signed Test Connection plus a short media test before opening a deployment.
Maintain matched database/config/object backups and patch runtime dependencies.
See storage/configuration/known-limitations docs for operational boundaries.
