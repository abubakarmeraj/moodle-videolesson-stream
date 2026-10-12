# Installing ValeLMS with an AI operations agent

Use the **same** [Quick Start](quick-start.md), [Compose](docker.md),
[storage/proxy examples](installation-examples.md) and [preflight](preflight.md)
as a human administrator. There is no AI-only installer or permission bypass.
This refines the independent tester's proposed guide with guarded configuration
generation, actual storage write checks and current protocol-2 guidance.

## Preserve existing state

Confirm the authorized target host and scope before any command. Inventory OS,
architecture, resources, ports, containers, existing Moodle and DB ownership
without printing private files. Capture a protected matched DB/config/moodledata
backup and restoration limits. Do not uninstall databases, delete directories,
reset volumes or change an existing proxy to make installation pass. Native
install refuses an unowned DB; use Compose or a separate host instead.
Do not use a production/cloud account merely because credentials are available.

## Choose and verify one matched version

Verify source/archive manifests and checksums before extraction. The coordinated
stable candidate is plugin **2026101201 / 3.1.0** + service **0.5.0**, protocol
**2**, migrations **001–005**. Candidate packages stay private until artifact
verification and human publication approval. Never mix branch files with frozen
assets or bypass version guards. RC1 component migration is not automatic;
read [upgrading](upgrading.md) for existing prerelease installations.
Use a supported Moodle patch/PHP/DB combination and record what you actually run.

## Use the documented workflow

1. Install the normal plugin ZIP. Observe its Video Service setup instructions.
2. Provision explicit private raw/processed buckets and restricted role credentials,
   browser-reachable trusted HTTPS storage/API/gateway, exact-origin CORS/ETag.
   Check storage distribution availability; MinIO is not bundled. SeaweedFS has
   a separately verified example, not automatic provisioning.
3. Run `deploy/setup.py` once with a **new**
   private directory; hidden prompts or a protected policy are supported. It
   invokes the existing preparer.
   Preserve the generated tenant/subject key and all config on retries.
4. Run local preflight, build the shared local image, start Compose and configure
   the reviewed HTTPS proxy. No changes to unrelated Moodle/DB/firewall/IAM.
   Before startup use `--check-ports`; for another stack follow the explicit
   [project/config/loopback-port example](installation-examples.md#two-independent-compose-stacks).
   Pass the same port variables on every Compose invocation and to preflight.
   Do not stop an existing application to resolve a collision.
5. Run explicit online/authenticated preflight and the tiny scoped write probe.
   HEAD/health alone are insufficient. Resolve actual-role permissions and storage
   volume capacity failures, not source-patch them. Do not log signed URLs.
6. Securely copy only the six-field connection JSON outside the Moodle webroot,
   directory 0750/file 0640 for the actual PHP group. Save the **path**, not
   contents, in Video Service configuration. Test Connection must be COMPATIBLE
   with schema/storage/Redis/capacity ready.
7. Teacher: native short synthetic upload → Ready. Enrolled student: decode,
   seeking, visible natural watch, persisted progress/completion after reload.
   No fabricated tracking/API/database credit. Separate visible/background
   observations using the [controlled plan](development/installation-ux/watch-progress-plan.md).

## Diagnose and report honestly

Distinguish intentional pause, retrying transport, storage HTTP failure, expired
**or denied** authorization and service request failure. Retain the same upload
session/file for resume. Never expose cookie/Authorization/RPC bodies, protected
JSON, full presigned URL or bearer media token in logs/screenshots/issues.

Record elapsed start/end, shell submissions (not falsely individual commands),
manually authored files, operator decisions, infrastructure vs documentation vs
product failures. PENDING/skipped checks are not PASS. Do not claim a faster
installation without a comparable timed fresh-host run. Failed evidence remains
distinct from final acceptance.

Rollback preserves data: no routine `down -v`, dropped schema or deleted bucket.
Stop only new services when appropriate and follow [uninstall](uninstall.md).
Destructive restoration needs explicit scope; restoring DB alone cannot restore
deleted media. Stop if continuing requires authority over another system.
