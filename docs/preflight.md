# Guided setup and non-destructive preflight

These tools ship in the coordinated 3.1.0 / service 0.5.0 candidate; older
published RC2 archives remain immutable. Install matched verified packages.
Compose >= 2.30 is required for raw env-file secret preservation. See
[Docker's format contract](https://docs.docker.com/reference/compose-file/services/#format).

## Protected configuration

From the approved source/service root on Linux:

```sh
sudo python3 deploy/setup.py --directory /etc/valelms-video
```

Requires an existing non-shared-writable parent. Prompts hide all role keys; no
secrets in process arguments or output. Creates directory 0700, policy/key files
0600, then calls the existing manifest-guarded Compose preparer to generate
runtime identities/configuration and private disk staging. It does not provision
buckets, install packages, edit Moodle, change firewall/IAM or start services.
Bucket names are explicit; raw and processed must differ. Defaults: S3 region
us-east-1 (R2 auto), path addressing. Advanced operators use:

```sh
sudo python3 deploy/setup.py --directory /etc/valelms-video \
  --config /protected/operator-policy.json
```

The existing policy retains `storage_region`, `storage_addressing_style` and
optional `storage_ca_bundle`. Generated runtime env files contain secrets; parent
directory stays root-only. The preparer keeps legacy variable names compatible
with runtime. A private storage CA also requires the documented read-only Compose
mount at `/run/video-ca/ca.crt`; do not disable TLS verification.

Rerun startup with the same config. Setup refuses existing directories/symlinks
and never rotates an installed tenant/subject key. On input failure a new partial
directory may remain: retain privately, inspect and choose a new setup directory
only if it has never been used. Do not delete an installed directory to bypass
the guard. Noninteractive CI uses synthetic `--config`, never production keys.

## Checks before/after startup

```sh
sudo python3 deploy/preflight.py --config /etc/valelms-video/policy.json \
  --staging /etc/valelms-video/runtime/staging
```

Default is local-only: Linux amd64/arm64, host resources, Docker daemon/Compose,
private policy validation and staging free space. It only reads state. A 1 GiB
free-disk check is a **small smoke prerequisite**, not video admission. The
runtime worker heartbeat still applies its source-size/duration/ladder estimate.
Preflight checks 0700 permissions and rejects tmpfs/ramfs using Linux mountinfo;
operators still review actual backing storage, container limits and workload
headroom. No giant tmpfs, no unsupported platform implied by a PASS.

Add `--online` to check DNS/trusted TLS for explicit operator origins and API/
gateway health. Add `--handoff` for signed protocol/schema/storage/Redis/worker
readiness. Run from the service host; repeat Test Connection from Moodle and a
browser upload from the actual client network. A server probe cannot prove
another host's reachability/trust.

Storage probes use the runtime's locked boto3 dependency, not a new runtime
dependency. On a host without that environment, prepare a dedicated operator
venv (install python3-venv using the OS package manager if absent):

```sh
sudo python3 -m venv /opt/valelms-tools
sudo /opt/valelms-tools/bin/pip install -r service/video-service/requirements.txt
sudo /opt/valelms-tools/bin/python deploy/preflight.py \
  --config /etc/valelms-video/policy.json --staging /etc/valelms-video/runtime/staging \
  --online --handoff /etc/valelms-video/runtime/moodle-connection.json --storage-probe
```

Explicit `--storage-probe` creates tiny random `valelms-preflight/<random>` keys
only in the two configured buckets: role HEAD, raw multipart create/presigned
part PUT/list/complete, worker read, processed write/HEAD, gateway normal/range
read, abort and janitor delete. It uses actual role keys, exact-origin OPTIONS
and PUT checks and requires exposed ETag. It does not enumerate bucket contents,
change IAM/CORS or delete other objects. Interrupted execution may leave a tiny
probe object/upload; use normal approved storage administration to review only
that prefix. Failure to clean up is a FAIL, not hidden success. Bucket versioning
or legal holds can retain deleted versions; this tool never purges them.

Before first startup add `--check-ports`, with `--api-port`/`--gateway-port` if
overriding defaults. This makes a collision actionable without stopping another
stack. Omit this check once your own stack is running. See [two-stack example](installation-examples.md#two-independent-compose-stacks).

JSON output contains only allowlisted check names/status/guidance; no exception
body, URL, key or signature. Exit 1 = a failed check; exit 0 means selected checks
passed, **not all installation/media checks passed**. PENDING is always explicit.
Preflight performs no database migration, package install or service restart.
