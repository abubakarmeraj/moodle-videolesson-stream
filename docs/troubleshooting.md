# Troubleshooting

Start with **Test Connection**, not screenshots of secrets or `/health` alone.

| Result | Check |
|---|---|
| SERVICE_UNREACHABLE | Exact HTTPS origin, DNS/TLS trust, private routing, API role |
| AUTHENTICATION_FAILED | Correct protected six-field file, matched stable tenant/keyid/key, time synchronization |
| SERVICE_TOO_OLD / SERVICE_NEWER_UNTESTED | RC2 plugin 2026100702 + service 0.5.0-rc2, protocol 2 (also used by unreleased dev.3); do not suppress the compatibility guard |
| SCHEMA_NOT_READY | Explicit migrator and001–005; retain DB, do not repair rows manually |
| STORAGE_NOT_READY | Private bucket access, endpoint/region/addressing, role keys, TLS trust |
| NO_WORKER_CAPACITY | Worker heartbeat, private staging space, configured limits and active job |

Upload failing before PUT: inspect sanitized Moodle/service authorization errors.
PUT failing: check browser-reachable HTTPS storage, exact-origin CORS and exposed
ETag. Never paste full signed URLs into reports. Processing failure: inspect
sanitized job status, actual media codec/duration, disk and lease state. A higher
upload setting cannot overcome insufficient staging. Reconciliation is idempotent;
do not manually delete a referenced video to clear an error.

## Upload messages (unreleased diagnostic improvement)

Only pressing **Pause** should report an intentional pause. A terminal storage
HTTP 500 is now a storage-transfer failure, not “Upload paused.” Temporary
network/timeout failures retry up to three part attempts with fresh authorization;
after that, select the **same file** to resume committed parts. Storage 401/403
means authorization expired **or denied**; HTTP status alone cannot distinguish
expiry from incorrect IAM. Moodle/service request failures are separate. Never
display raw provider response text or full presigned URLs.

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
