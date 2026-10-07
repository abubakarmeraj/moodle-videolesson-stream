# ValeLMS Video Lesson Stream RC2 — Local qualification

2026-10-07. **GO for private Local qualification candidates, not public release
or full media/deployment readiness.** Owner-approved activity identity is
`mod_videolessonstream` / `videolessonstream`. The invalid requested underscore
spelling is historical evidence only; native Moodle core was never patched.

## Provenance and scope

Starting source770fc98b789abfcbf56eb3d26fddbf8b615ec4c9 on
codex/valelms-stream-rc2. Immutable RC1 tag v3.1.0-rc1 remains at
3c2f59f704421f199033f020fd60eec50ea84a8d; its packaged source is
bd41c0bd529848d2da10d105dd3dd74f109d5050. Historical manifests/reports are
retained under docs/release/rc1 and docs/development/rc1. No remote rename,
release/tag push, public artifact or hosted/Golden LMS action was performed.

Both immutable RC1 archives retain their verified hashes: plugin
0a1168c3ad40a4aabf4b166d85ad9a6e4945dac765959cb1107eec7b6c1622a0;
service fbf2e5c250d4dba47cc64867988c13ad61d8c92d73c1ff2dd28ce97d650b7802.
The artifact release manifest identifies the exact clean RC2 source commit;
do not infer it from the original RC1 tag or an uncommitted checkout.

## Identity and isolation

Plugin2026100702 / ValeLMS3.1.0-rc2; service0.5.0-rc2; protocol2;
service schema001–005. Display name ValeLMS Video Lesson Stream. All component
callbacks/PHP namespaces/config/capabilities/URLs/language/templates/tasks/
backup/restore/AMD source/build/maps use the approved identity. All13 tables
are disjoint from RC1; longest names remain under28 characters. Internal
keys and Moodle DML follow the explicit table map. No RC1 table adoption,
destructive upgrade or automatic cross-component migration is shipped.

Before branding scan:145 occurrences in starting tracked source. Final counts
and classification of every remaining brand/component hit are authoritative in
IDENTITY-OCCURRENCES.json; scopes differ because RC1 history copies were added.
No current executable/UI old-brand hit is permitted except explicitly tested
protocol1 aliases and the detector itself. Per-file old/new path/hash delta is
RC1-DELTA.json. Unchanged third-party grants, libraries, PNG artwork, dependency
lock and service migrations are checked against RC1. GPL-3.0-or-later is unchanged.
Project notices follow owner authorization; upstream ownership is not rewritten.
Security contact remains abubakar.meraj11@gmail.com.

## Native Moodle evidence

Brand-new application clone, DB and moodledata in the independent development
environment, Moodle5.2.2 Build20260810, core
acfa383c13dd46c83ca82894a8e95fac273fda33. PHP8.3.6, MariaDB-backed Moodle.
Moodle discovers only the new component before the explicit coexistence fixture
is introduced. Supported CLI install succeeds. All13 XMLDB tables, four
capabilities, reconcile task, service/storage admin pages, language, active player
template, three native AMD request registrations, completion/privacy/event
autoload and backup/restore class discovery pass. Native add_moduleinfo creates
the activity and its durable pending intent. No unexpected upgrade is pending.

The published GPL RC1 ZIP was installed alongside RC2 as a private predecessor
fixture. All26 tables, two module/version registrations, four capabilities each,
independent config, PHP callbacks/autoload and tasks pass. RC1 extracted source
bytes remain unchanged. This is **not** a claim that every pristine upstream
release has been runtime-tested. Static original table/capability/component
collision audit is complete; Deployment can use a reviewed original fixture.

Initial failed tests were harness initialization issues (backup base classes
were not explicitly included by the CLI harness); fixing the harness, not core
or product backup behavior, made them pass. Historical invalid-name logs remain
separate from final acceptance evidence.

## Signed setup and security

Native renamed real_provider Test Connection → actual new service ASGI route
over locally trusted HTTPS: COMPATIBLE. Peer/host verification stays enabled.
Real isolated service MariaDB migrations001–005 and nonce uniqueness, plus a
private Redis namespace, are used. Wrong-key authentication is denied and replay
of a committed nonce across protocols is rejected by the real DB. **Storage
readiness is a test-only stub**, not live R2/MinIO media or browser setup evidence.
No cloud credentials/requests are required by these tests.

New clients sign POST,/v2/rpc,key ID,time,nonce,SHA256(body) with HMAC-SHA256 and
X-VL-Key/Time/Nonce/Signature. Duplicated or mixed families fail closed. Legacy
/v1/rpc X-CF aliases and old grants are allowed only by explicit
SERVICE_ALLOW_LEGACY_PROTOCOL=true; false disables both. Signature/expiry/tenant
checks and replay storage remain intact. New grants use videolesson-stream-media.
The six protocol tests include wrong body/path/signature/family, replay, audience,
expiry and tenant negatives. Redis namespace changes are defaults only; existing
explicit namespaces are not migrated or rewritten.

## Fast qualification and packaging

32 Python tests,126 PHP syntax checks,35 JS syntax checks, six PHP compatibility
cases and ten compiled-uploader URL-security cases pass. All15 AMD modules and
maps reproduce exact bytes from pinned Babel7.28.0/transform-AMD7.27.1/Terser5.43.1.
Source build used Node24.17.0; independent Linux reproducibility used Node18.19.1.
XMLDB/third-party XML and all three project SVGs parse with local-asset guards.
The module-name negative test prevents packaging the rejected underscore form.
PHPCS is unavailable and is not claimed as passed. Private/credential scans are
bounded signatures plus reviewed path inventory, not universal secret detection.

Candidates are built twice from the exact clean Local checkpoint. The ignored
private release-level RELEASE-MANIFEST.json and SHA256SUMS record exact commit,
filename,size,entry count,archive and embedded-manifest hashes. Build tooling
rejects dirty public source, invalid module names, unsafe members, unexpected
symlinks/special nodes and manifest drift. No artifact is published or replaces RC1.
Final private evidence records independently extracted payload comparisons,
artifact-native syntax/version/layout checks and a Moodle code-replacement smoke.

## Handoff and limits

R2 remains first-class (strict endpoint,auto/SigV4/path defaults, separate private
buckets). Dedicated synthetic endpoint/client/presign/multipart/HEAD/range/delete
regressions pass. Generic S3 configuration/readiness/URL tests pass. This is not
a new live R2 test or an assertion that all S3 providers are equally qualified.
Ordinary-server deployment, real CORS/browser upload and the short complete
media/renewal/progress/completion/recycle smoke remain Deployment's responsibility.

No broad media matrix, production credentials, hosted connection, Golden LMS
mutation, Moodle-core patch or publication action occurs in Local. Core tracked
source is clean. Independent disposable state and failed evidence are retained.
Read RC2-QUALIFICATION-HANDOFF.md and docs/rc1-to-rc2.md before downstream testing;
RC1 is not automatically upgraded and must not be uninstalled to force migration.
