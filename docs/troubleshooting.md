# Troubleshooting

Start with **Test Connection**, not screenshots of secrets or `/health` alone.

| Result | Check |
|---|---|
| SERVICE_UNREACHABLE | Exact HTTPS origin, DNS/TLS trust, private routing, API role |
| AUTHENTICATION_FAILED | Correct protected six-field file, matched stable tenant/keyid/key, time synchronization |
| SERVICE_TOO_OLD / SERVICE_NEWER_UNTESTED | Stable plugin 2026101201 + service 0.5.0, protocol 2; upgrade the matched pair, never suppress compatibility guards |
| SCHEMA_NOT_READY | Explicit migrator and001–005; retain DB, do not repair rows manually |
| STORAGE_NOT_READY | Private bucket access, endpoint/region/addressing, role keys, TLS trust |
| NO_WORKER_CAPACITY | Worker heartbeat, private staging space, configured limits and active job |

Upload failing before PUT: inspect sanitized Moodle/service authorization errors.
PUT failing: check browser-reachable HTTPS storage, exact-origin CORS and exposed
ETag. Never paste full signed URLs into reports. Processing failure: inspect
sanitized job status, actual media codec/duration, disk and lease state. A higher
upload setting cannot overcome insufficient staging. Reconciliation is idempotent;
do not manually delete a referenced video to clear an error.

## Upload messages

Only pressing **Pause** should report an intentional pause. A terminal storage
HTTP 500 is now a storage-transfer failure, not “Upload paused.” Temporary
network/timeout failures retry up to three part attempts with fresh authorization;
after that, select the **same file** to resume committed parts. Storage 401/403
means authorization expired **or denied**; HTTP status alone cannot distinguish
expiry from incorrect IAM. Moodle/service request failures are separate. Never
display raw provider response text or full presigned URLs.

After terminal failure the headline becomes **Status: Failed**, with the useful
sanitized message retained across polling. Intentional Pause has its own paused
headline. Reload reconstructs the durable server upload and permits same-file
resume; a local transfer failure does not destroy the multipart session.

## Compose port collision

Run preflight `--check-ports` before first startup. Default API/gateway loopback
ports are 28090/28091; a second stack can use 28190/28191 through
`VIDEO_API_PORT`/`VIDEO_GATEWAY_PORT`. Match preflight arguments and HTTPS upstreams.
Use a distinct Compose project and protected configuration; keep MariaDB/Redis
unpublished. See [the concrete example](installation-examples.md#two-independent-compose-stacks).
An already-running own stack is expected to occupy its ports: omit the prestart
check after startup. Never stop another application or delete a volume to proceed.

A successful PUT without a browser-readable ETag requires storage CORS correction.
Network errors can also hide a CORS failure: inspect sanitized status/header
categories, not bearer URLs. Status polling must not erase the failure message.

## Storage health is not storage write capacity

Test Connection checks signed compatibility and bucket HEAD/readiness, **not**
multipart writes. Run the opt-in [preflight write probe](preflight.md) with actual
role credentials before the short browser upload. The independent SeaweedFS test
had healthy HEAD but PUT 500 because the volume limit could not satisfy the
allocation batch. It also needed API permission to HEAD **both** buckets. Fix
the infrastructure cause; do not patch Moodle or restart/delete an upload session.
The same session resumed after the storage correction.

If a pinned image/FFmpeg package is unavailable, review/update/requalify it rather
than removing the pin silently. Keep old application/config state for rollback.
Report versions, status categories and sanitized logs without cookies, credentials,
student data, raw RPC payloads or bearer media URLs.
