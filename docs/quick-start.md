# Install ValeLMS: plugin, service, then a test video

ValeLMS needs a Moodle plugin **and** a Linux Video Service. You do not need a
ValeLMS account. You do need private S3-compatible storage, role credentials,
DNS/trusted HTTPS and enough private processing disk. [Requirements](installation.md).

Use one matched **3.1.0** package pair: plugin 2026101201 and service 0.5.0,
protocol 2, migrations 001–005. Verify the supplied `SHA256SUMS` before extracting.
During stable preparation these packages are private candidates, not a published
release. Existing installations: read [upgrading](upgrading.md); do not mix files
or manually patch an older distribution.

## 1. Install the plugin normally

Install `mod_videolessonstream-3.1.0.zip` through Moodle and complete its normal
upgrade screen/CLI. It adds **ValeLMS Video Lesson Stream**, not the older
`mod_videolesson`. [RC1 transition](rc1-to-rc2.md).

## 2. Install the separate service

Use [Docker Compose on the existing Moodle host or a separate Linux server](docker.md).
Provision private storage and trusted HTTPS first; [examples](installation-examples.md)
cover generic S3/SeaweedFS, role permissions and the reverse proxy.

Extract `valelms-video-service-0.5.0.tar.gz`; from its `video-lesson/` root:

```sh
sudo python3 deploy/setup.py --directory /etc/valelms-video
sudo python3 deploy/preflight.py --config /etc/valelms-video/policy.json \
  --staging /etc/valelms-video/runtime/staging --check-ports
```

The guide asks for four HTTPS origins, backend, two bucket names and four pairs
of role credentials (hidden input). It creates protected files; no IAM, buckets,
Moodle, firewall or services are changed. Existing config is never overwritten.
For a non-default region/addressing/private CA, supply the protected operator
policy instead. Run the documented Compose **build**, then **start**, commands.

After startup and HTTPS routing, run the full explicit checks using the service's
locked Python environment (see [preflight](preflight.md)):

```sh
sudo /opt/valelms-tools/bin/python deploy/preflight.py \
  --config /etc/valelms-video/policy.json --staging /etc/valelms-video/runtime/staging \
  --online --handoff /etc/valelms-video/runtime/moodle-connection.json --storage-probe
```

`--storage-probe` briefly creates/deletes tiny random synthetic objects. It never
changes bucket policy or deletes existing media. Fix FAIL results; do not treat
PENDING checks as verified. The local-only run can precede service startup.

## 3. Connect Moodle and upload a short video

Securely copy only `runtime/moodle-connection.json` to the Moodle server, outside
webroot: root:PHP-runtime group, directory 0750, file 0640. Do not paste its
contents into a browser or issue report. In **Site administration → Plugins →
Activity modules → Video Service configuration**, enter its local path and click
**Test Connection**. Require COMPATIBLE, schema 001–005, both buckets, Redis and
fresh worker capacity. `/health` alone is insufficient.

Create a lesson as a teacher → Save and display → Upload Video → wait for Ready.
Use an enrolled student to check playback and saved watch progress/completion.
That short browser test is essential: a service-host probe cannot prove browser
DNS/TLS/CORS or Moodle-host connectivity. [Troubleshooting](troubleshooting.md).
