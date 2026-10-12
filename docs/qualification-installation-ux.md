# Independent installation-UX verification (2026-10-12)

This is supplied real Ubuntu evidence for **78094377079b73167cc4013d559b9c6101489d48**,
plugin 2026101200 / 3.1.0-dev.3 + service 0.5.0-rc2. It is **not** testing of the
later stable package or permission for Video Local to connect to that VM.
The original private REPORT.md and VIDEO-LOCAL-HANDOFF.md remain unchanged.

Result: **PASS_WITH_NONBLOCKING_UX_FINDINGS**, ready for focused stable preparation.
Ubuntu 24.04.5 ARM64, Moodle 5.2.4, PHP 8.3.6, MariaDB 10.11.14, Docker 29.9.0 /
Compose 5.6.0, SeaweedFS 4.48, packaged FFmpeg 5.1.9. Fresh independent application,
database/data/configuration, tenant, service volumes and storage; prior accepted
installation and its data/configuration were preserved.

Passed native plugin installation, real guided configuration (7 visible answers,
8 hidden keys), local/online preflight, role storage write/read/CORS negative,
signed Test Connection, upload → processing → HLS playback → enrolled student
progress/completion. Teacher/student service-config access was denied. Candidate
payload inventories matched after testing: 237 plugin and 112 service-bundle files.

Browser cases: persistent storage 500, blocked CORS, network disconnect and missing
ETag gave sanitized useful messages, not false pause. Automatic retry recovered;
intentional multipart Pause/reload/same-file resume succeeded. Clean ETag recovery
reused the committed part without another PUT. A 45,079,733-byte source resumed to
Ready with exact stored content. A 20-second visible student play persisted [0,20],
20 watched seconds and completionstate 1 after reload.

Three follow-ups: setup heading missing from first-install New settings (present
in normal settings); no clickable documentation in the five steps; terminal
upload failure still headlined Uploading. A second Compose stack also needed
an undocumented port override. These are the bounded stable-preparation changes.

One initial fault proxy returned incorrect zero Content-Length on HEAD; its
contaminated recovery trial was discarded. Proxy corrected, preflight repeated,
and clean recovery passed with no product/DB repair. An initially missed Pause
was also repeated while transfers were active. Neither is converted into a PASS.

Observed baseline-to-first-play **11m27s** versus prior **20m23s** (~44% lower).
This is not isolated causal proof: experienced operator, preinstalled host tools,
cached archive/images and overlapping steps differ. 11 remote submissions through
first play / 35 including expanded diagnostics; 6 installation configuration files
/ 7 including diagnostic unit. Full sessions are not comparable broad benchmarks.

The tester did not investigate background-credit policy, endurance, multi-GiB or
a new cross-browser matrix. No stable publication approval was given. Private
hosts, credential paths, backups, cookies and signed URLs are excluded here.
