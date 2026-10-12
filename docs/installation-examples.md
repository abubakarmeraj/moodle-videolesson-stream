# Existing Moodle + Compose + private S3: complete configuration examples

Examples are operator-reviewed templates, **not automatically applied**. Replace
example.invalid names and bucket placeholders. Preserve existing Moodle/DB/
proxy configuration; obtain matched recovery first. Use separate service data,
protected paths and a unique Compose `-p` name if another stack exists. Do not
publish DB/Redis, storage master/filer/volume or administration consoles.

## Ubuntu 24.04 with existing Moodle

Install the matched plugin ZIP normally. On the service host, provide Docker,
Compose, Python 3.12, private buckets and trusted HTTPS. The service uses its own
MariaDB schema/volume—never point it at Moodle's schema. Follow [guided setup](preflight.md)
or RC2's [manual Compose policy](docker.md), then build the local image before
`up -d --no-build`. Use the storage-network overlay. Copy only the six-field
handoff to a root:PHP-group 0640 file under a 0750 directory outside webroot.

## Trusted HTTPS reverse proxy

The Compose proxy binds API `127.0.0.1:28090`, gateway `127.0.0.1:28091`.
This operator Nginx example assumes you have already provisioned valid certificates.
Use separate server blocks for the storage endpoint. Do not proxy binary uploads
through Moodle/PHP or through the Video API. Do not enable request-body logging.

```nginx
server {
    listen 443 ssl;
    server_name video.example.invalid;
    ssl_certificate /etc/letsencrypt/live/video.example.invalid/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/video.example.invalid/privkey.pem;
    access_log off;
    error_log /var/log/nginx/valelms-api-error.log crit;
    client_max_body_size 1m;
    location / {
        proxy_pass http://127.0.0.1:28090;
        proxy_set_header Host $host;
        proxy_read_timeout 60s;
    }
}
server {
    listen 443 ssl;
    server_name media.example.invalid;
    ssl_certificate /etc/letsencrypt/live/media.example.invalid/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/media.example.invalid/privkey.pem;
    access_log off;
    error_log /var/log/nginx/valelms-media-error.log crit;
    location / {
        proxy_pass http://127.0.0.1:28091;
        proxy_set_header Host $host;
        proxy_buffering off;
        proxy_read_timeout 60s;
    }
}
```

Validate candidate Nginx configuration before reloading your proxy; these tools
do not do it for you. Access/error logs elsewhere in the proxy chain can still
record request URLs: review the whole chain, especially media and signed S3 paths.
Health HTTP 200 does not establish authentication or storage writes.

## Generic S3 and role permissions

Use `deploy/operator-policy.json.example`: `s3-compatible`, HTTPS endpoint visible
to both service and browser, explicit region, path or virtual addressing, distinct
private buckets and four role credential pairs. No Cloudflare account is needed.
All runtime roles use the same externally valid endpoint; internal-only container
names/localhost are not usable browser destinations. Presigned Host/path/query
must survive any TLS proxy **unchanged**.

| Role | Raw bucket | Processed bucket |
|---|---|---|
| API | Multipart create/upload/list/complete/abort, HEAD/verification, scoped abort deletion | Bucket HEAD for readiness; no processed writes/deletes |
| Worker | HEAD/read source | Put/HEAD/read generated objects |
| Gateway | No raw-object access | HEAD/read/range |
| Janitor | List/HEAD/read/delete assigned expired objects, abort abandoned uploads | List/HEAD/read/delete assigned expired objects |

For AWS-style IAM, bucket HEAD maps to `s3:ListBucket`; object PUT permissions
cover multipart initiation/parts/completion, plus explicit
`s3:ListMultipartUploadParts` and `s3:AbortMultipartUpload` as needed. Keep bucket
and object ARN scopes distinct; do not copy admin credentials into runtime roles.
This API policy template illustrates the distinction (replace both bucket names):

```json
{"Version":"2012-10-17","Statement":[
  {"Effect":"Allow","Action":["s3:ListBucket"],"Resource":["arn:aws:s3:::videolesson-private-raw","arn:aws:s3:::videolesson-private-processed"]},
  {"Effect":"Allow","Action":["s3:GetObject","s3:PutObject","s3:DeleteObject","s3:AbortMultipartUpload","s3:ListMultipartUploadParts"],"Resource":"arn:aws:s3:::videolesson-private-raw/*"}
]}
```

Apply analogous worker/gateway/janitor grants from the table using your provider's
permission model. Source operations can need additional encryption-key permissions
if the operator enables KMS. [AWS HeadBucket permissions](https://docs.aws.amazon.com/AmazonS3/latest/API/API_HeadBucket.html)
and [multipart permissions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html)
are provider references, not a claim that every S3 implementation is identical.

## Exact-origin CORS

Operator-applied raw bucket example; no public-read grant:

```json
{"CORSRules":[{"AllowedOrigins":["https://moodle.example.invalid"],
"AllowedMethods":["PUT","GET","HEAD"],"AllowedHeaders":["Content-Type","x-amz-*"],
"ExposeHeaders":["ETag"],"MaxAgeSeconds":3600}]}
```

The browser needs PUT/OPTIONS with the actual headers and visible ETag. GET/HEAD
are included for an operator smoke; media is normally delivered through the
authorized gateway, not a public processed bucket. Do not replace exact origin
with `*`. Preflight performs OPTIONS **and** an actual signed PUT. Consult
[S3 CORS elements](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ManageCorsUsing.html).

## SeaweedFS 4.48: independently verified example

The separate Ubuntu ARM64 test used the official 4.48 `linux_arm64.tar.gz`
archive, SHA-256 `557e92c38c5c7d180748eb8e2b2b45e426f8e5282a4caca8e098a90d09f03a07`.
Do not assume this digest applies to other architectures/releases. Obtain and
verify your chosen build from the [official release](https://github.com/seaweedfs/seaweedfs/releases/tag/4.48).
ValeLMS does not bundle/download or maintain the storage server.

Run as a dedicated unprivileged storage user with a private persistent data
directory and protected role-identity JSON. The verified command shape was:

```sh
weed server -dir=/srv/valelms-storage/data -ip=127.0.0.1 -ip.bind=127.0.0.1 \
  -master.telemetry=false -master.volumeSizeLimitMB=128 -volume.max=16 \
  -filer -s3 -s3.port=29000 -s3.config=/etc/valelms-storage/s3.json
```

These small-volume values are the short synthetic test, not production sizing.
Do not use `volume.max=3` with a default seven-volume growth batch: HEAD can pass
while PUT returns 500. Plan enough capacity for **both** bucket collections and
verify writes. The [upstream S3 guide](https://github.com/seaweedfs/seaweedfs/wiki/Amazon-S3-API)
explains per-bucket volume growth. That sizing is a storage-operator decision.

SeaweedFS identity JSON has `identities[]`, each with `name`,
`credentials:[{"accessKey":"REPLACE","secretKey":"REPLACE"}]`, and `actions`.
Keep real JSON root:storage-group 0640 under 0750, never in source/webroot. The
verified bucket-scoped action sets were:

| Role | SeaweedFS actions (substitute bucket names) |
|---|---|
| API | Read:raw, Write:raw, List:raw, Read:processed, List:processed |
| Worker | Read:raw, List:raw, Read:processed, Write:processed, List:processed |
| Gateway | Read:processed, List:processed, List:raw (historical test configuration; no Read:raw) |
| Janitor | Read:raw, Write:raw, List:raw, Read:processed, Write:processed, List:processed |

SeaweedFS coarse actions are broader than fine-grained AWS IAM. The API's
`Read:processed` was needed for bucket HEAD; evaluate provider-specific finer
policies before multi-tenant deployment. Do not claim only object-free access
from a coarse grant. See [4.48 authorization code](https://github.com/seaweedfs/seaweedfs/blob/4.48/weed/s3api/s3api_server.go).
Use a separate private provisioning identity to create buckets/CORS, not API
Admin permission. Buckets stay private; anonymous access must be denied.

TLS proxy storage.example.invalid to loopback 29000 with unchanged Host/query,
`client_max_body_size 0` (part limits are signed/service-controlled),
`proxy_request_buffering off`, adequate PUT timeout and disabled sensitive URL
logging. Do not publish SeaweedFS administrative/master/filer/volume ports.
Provision certificates and CORS before running the write probe and browser test.

MinIO remains supported; the tester encountered unavailable image/binary URLs.
Use an operator-supported distribution, not an assumed bundled dependency.
