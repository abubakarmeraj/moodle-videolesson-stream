# One focused stable artifact-native verification

This is the next Deployment phase, **not publication approval**. Use the single
private matched packet containing `mod_videolessonstream-3.1.0.zip`,
`valelms-video-service-0.5.0.tar.gz`, SHA256SUMS, outer RELEASE-MANIFEST.json and
release notes. The outer manifest supplies the exact committed source and hashes;
do not build a competing candidate or patch an existing live installation.

## Scope

Use one disposable real Ubuntu 24.04 lane with supported Moodle 5.2.4, private
S3-compatible storage and trusted HTTPS. Existing working Load Tester/Golden LMS
or other installations require separate authority; preserve all existing code,
DB/data/configuration, ports and storage. No broad historical/media/endurance replay.

1. Verify both outer checksums, safe archive paths/types and every embedded
   manifest entry. Confirm plugin 2026101201 / ValeLMS 3.1.0 / STABLE maturity,
   service 0.5.0 / protocol 2 / migrations 001–005. No006; lock/license notices intact.
2. Fresh native Moodle ZIP install → Continue → **New settings**: verify
   “Set up video uploads” and an actionable Video Service configuration link are
   actually present here, not just on the normal settings page. Save defaults;
   follow the link, click each of the five documentation links and check correct
   HTTPS targets, safe new tabs and usability. Guides track public main; exact
   candidate instructions are also inside the service package. No automatic
   external fetch is introduced by these links.
3. Administrator can save the protected path/Test Connection. Teacher and student
   cannot access configuration or change service identity. Confirm compatible
   stable pair, schema, raw/processed, Redis and fresh worker capacity. Old RC2
   service must be classified TOO_OLD, not accepted by weakening the guard.
4. On a second isolated stack use independent config/project/tenant/buckets and
   VIDEO_API_PORT=28190 / VIDEO_GATEWAY_PORT=28191 (or other unused pair).
   Preflight --check-ports must clearly fail an occupied or duplicate port; choose
   another pair, never stop an unrelated service. Verify only loopback bindings
   and no published DB/Redis. Match TLS upstreams, retain variables on restart.
5. Through a disposable sanitized fault injector, exhaust all three part attempts
   with HTTP500: both **Status: Failed** and the useful storage-failure message
   must remain after polling. Repeat a bounded network/CORS or missing ETag case.
   No raw provider text or full signed URL/credential may appear.
6. One transient fault recovers automatically. Intentional Pause shows paused,
   same file after reload resumes server-confirmed parts and reaches Ready.
   One small native upload/processing/HLS playback and persisted student completion
   is sufficient continuity smoke. No long media/multi-GiB/broad engine matrix.
7. Confirm actual source still matches package manifests, no unexplained core,
   schema or service runtime changes. Save sanitized evidence and final verdict.

For an existing disposable RC2/dev.3 upgrade analogue, normal Moodle CLI upgrade
records only the supported savepoints to 2026101201. Service 0.5.0 uses existing
migrations 001–005 with no new migration; preserve identity/config/state. Normal
native installer refuses silent changed-source adoption; do not erase DB to force it.

Known limits and the unproven background-watch-credit observation remain explicit.
No player/completion policy change is authorized by this checklist.

Return PASS/FAIL for exact artifact identity, first-install navigation, all guide
links, admin-only access, failure headline persistence, pause/reload/resume,
alternate-port isolation, stable compatibility and short smoke. Record exact
source commit, archive/manifests/checksums and any unexecuted check as PENDING.
Only after this focused verification should the human approve stable publication.
