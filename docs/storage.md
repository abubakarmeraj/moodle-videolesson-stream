# Private storage: Cloudflare R2 and S3-compatible backends

Supported modes are `r2` and `s3-compatible`; local filesystem is **not implemented**.
Cloudflare R2 is a **first-class supported backend**, with a dedicated strict
account-endpoint validation and SigV4 configuration path.
Generic S3 requires an operator-configured HTTPS origin, region, path/virtual
addressing and separate private raw/processed buckets. MinIO was the qualification
implementation, not a promise that every S3 provider is certified, and not bundled.

## Cloudflare R2 — First-class support

Create separate private raw and processed buckets in your own Cloudflare account.
No ValeLMS account or public bucket is required. Operator policy selects
`storage_backend: "r2"`, the account's exact endpoint
`https://<32-lowercase-hex-account-id>.r2.cloudflarestorage.com`, and the raw/processed
bucket names. The account identifier is an endpoint input, not a Moodle secret.
The R2 path defaults to region/signing `auto`, SigV4 and path addressing.
Do not substitute a public custom-media domain for the authenticated S3 endpoint.

Provision bucket-scoped role credentials outside Moodle using protected
`storage_access_file` / `storage_secret_file` policy files. Direct service
configuration supports `R2_ENDPOINT`, `R2_ACCESS_KEY[_FILE]`,
`R2_SECRET_KEY[_FILE]` compatibility inputs, or generic `STORAGE_*` equivalents;
conflicting aliases are rejected. Secret keys stay server-side. Browser part
URLs contain only short-lived exact-bucket/key/upload/part authorization.

R2 regressions are release-critical: endpoint/client construction, SigV4 part
signing, multipart completion, HEAD/range/read/delete and raw/processed separation.
RC2 Local uses synthetic credentials/client stubs, **not a new live R2 cloud test**.
Historical dedicated R2 qualification is provenance, not proof about your account.

## Generic S3-compatible storage

Select `storage_backend: "s3-compatible"`, your browser/service-reachable HTTPS
`endpoint`, `storage_region` and `storage_addressing_style` (`path` or `virtual`).
Use separate private buckets and protected storage credential files. Provider
multipart/checksum/metadata/CORS behavior must satisfy the contract below.

## MinIO qualification

Independent prior qualification used a disposable HTTPS MinIO implementation.
MinIO is not bundled and its administration console must remain private. Local
RC2 retains configuration/client/URL tests; Deployment repeats one real upload
smoke after the identity/protocol change. No universal S3 compatibility claim.

The service's `STORAGE_ENDPOINT` must be reachable by both service and teacher
browser: it appears in short-lived exact-part presigned PUT URLs. A container-only
hostname or service-local localhost will not work for a remote browser. The API
never accepts a teacher-chosen endpoint. TLS verification stays enabled; an optional
CA bundle may trust a private CA. Browser uploads require HTTPS even if an explicit
development-only service HTTP setting is used for storage-layer tests.

## Access and CORS

- API: raw multipart creation/list/complete/abort, HEAD/verification and narrowly
  scoped raw deletion for verified abort cleanup; no processed deletion.
- Worker: raw read and processed write; gateway: processed read only.
- Janitor: scoped cleanup in assigned buckets; no bucket-wide arbitrary deletion.
- Buckets remain private. The MinIO admin console must not be publicly exposed.

Allow CORS for the **exact Moodle HTTPS origin**, PUT and actual headers
(`Content-Type` and any signed headers used by the provider), exposing **ETag**.
Browsers preflight with OPTIONS; allow the provider to answer it. Add GET/HEAD
only where the selected browser flow requires them. Do not use wildcard origins
as a substitute for testing. R2/bucket CORS and provider-level CORS differ; the
privately tested MinIO build used `MINIO_API_CORS_ALLOW_ORIGIN` because bucket CORS
configuration was unsupported. Consult the chosen version's operator documentation.

Signed Host, path and query must survive proxying unchanged. Do not rewrite a
presigned hostname after signing. Access-key identifiers may appear only as
required in SigV4; secret keys never leave the backend. Full presigned URLs are
temporary bearer credentials: do not record them in access logs or issue reports.

Storage must support multipart create/part/list/complete/abort, ETag, HEAD metadata
and exact sizes, ranged/normal GET and idempotent scoped delete. Adaptive sizing
plans at most 8192 parts; resume discovers committed parts, not browser-only state.
Readiness checks bucket access; a short real browser upload remains required to
verify CORS/network/provider behavior.
