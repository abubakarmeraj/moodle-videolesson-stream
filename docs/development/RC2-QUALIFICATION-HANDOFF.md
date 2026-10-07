# RC2 qualification handoff — private candidates, not publication approval

Owner-approved identity: **mod_videolessonstream**, Moodle directory
**videolessonstream**, display **ValeLMS Video Lesson Stream**. The previously
requested underscore spelling was rejected by native Moodle; it is not shipped.
[Historical blocker evidence](rc2/BLOCKER-RESULTS.md) is preserved.

Plugin2026100702 / ValeLMS3.1.0-rc2; service0.5.0-rc2; protocol2. Source and
payload hashes are authoritative in docs/release/IDENTITY.json, PRODUCT-MANIFEST,
SERVICE-MANIFEST and PUBLIC-SOURCE-MANIFEST. Private archive checksums, byte sizes,
embedded manifests and exact source commit are in the generated release-level
RELEASE-MANIFEST.json, accompanying SHA256SUMS and Local final evidence.

## What Local proves

Native disposable Moodle5.2.2 discovery/install, all13 XMLDB tables, four
capabilities, task/config/admin pages, language, templates, AMD requests,
backup/restore class discovery and native add_moduleinfo creation with durable
pending intent. Native provider Test Connection uses signed HTTPS with peer/host
verification, real isolated MariaDB nonce storage and Redis; bucket readiness is
explicitly a test-only stub, not live storage qualification. Wrong-key denial and
cross-protocol nonce replay are tested. Full media qualification is not repeated.

The public GPL RC1 predecessor ZIP is the private coexistence fixture; that is
not independently verified pristine upstream. Do not generalize its result to
every original-plugin release. RC1 data is not automatically migrated. Preserve
separate writable service tenants/state and explicit existing Redis namespaces.
Read [transition](../rc1-to-rc2.md) before touching an existing prerelease site.

## Deployment's bounded qualification

1. Verify both exact private candidate archives and embedded inventories; install
   `mod_videolessonstream-3.1.0-rc2.zip` normally into a fresh Moodle environment.
2. Check component/table/capability/config/file/task/backup isolation; qualify
   pristine original-plugin coexistence only if a reviewed fixture is available.
3. Deploy the matched service tarball, locked requirements and migrations001–005.
   No migration006 exists. Use the protected server-local handoff and Test Connection.
4. Require `/v2/rpc` and X-VL-Key/Time/Nonce/Signature. Preserve exact signed route,
   shared nonce replay rejection and `videolesson-stream-media` grant audience.
   Legacy `/v1/rpc`/X-CF aliases and old grants are temporary, authenticated and
   disabled by SERVICE_ALLOW_LEGACY_PROTOCOL=false. Do not mix header families.
5. Repeat dedicated synthetic R2 regressions; do not label them a live cloud test.
   Use exact operator-owned HTTPS R2 endpoint/auto/path configuration if later
   authorized. No cloud credentials are required by this handoff.
6. Run one independent HTTPS MinIO upload → processing → HLS → playback →
   progress/completion → recycle/recovery smoke. Validate browser reachability,
   CORS/ETag, private buckets, signed URLs, renewal and zero vendor/player-CDN egress.
7. Check the renamed settings action and teacher/student branding/permissions,
   library/relink, thumbnails, player controls, deletion/shared-reference safety
   and a bounded backup/restore smoke on the new namespace.
8. Verify classified old-brand/private/secret scan and RC1 checksums unchanged.

Do not repeat all historical OS3 work. Do not rename the remote, publish artifacts,
push a release tag or submit to Moodle until separate publication authorization.
