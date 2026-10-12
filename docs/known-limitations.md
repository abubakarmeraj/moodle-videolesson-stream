# Known qualification limits

- RC1 and RC2 are prereleases, not stable software. RC2 is a distinct Moodle
  component and does not automatically migrate RC1 activities, media or data.
- Ubuntu 24.04 WSL2 and a separate real Ubuntu 24.04.5 ARM64 VM **Compose**
  installation were qualified. The latter used Moodle 5.2.4/PHP 8.3.6/MariaDB
  10.11.14 and SeaweedFS 4.48; see [the separate evidence](qualification-ubuntu-arm64.md).
  Ordinary-server native/systemd and arbitrary operating systems remain unqualified.
- The exact RC2 artifacts passed fresh Moodle 5.2.2/PHP 8.3.6 installation,
  published-RC1 coexistence, signed setup, real HTTPS MinIO multipart upload,
  FFmpeg/HLS playback, seeking, progress/completion and recycle/recovery.
- Chromium was exercised in this focused RC2 qualification; no complete new
  Firefox/WebKit matrix is claimed. Older browser evidence is historical.
- Compose passed the full short synthetic-media lifecycle. Native/systemd passed
  fresh installation, restart, rerun, TLS, authenticated readiness and capacity
  checks; the media lifecycle was not duplicated on that lane.
- Six-hour endurance, multi-GiB stress and full-disk exhaustion are not qualified.
- Dedicated synthetic R2 regressions passed; no new live Cloudflare R2 test was
  performed for RC2. This does not qualify a particular operator's account.
- Generic S3 compatibility depends on the actual provider's TLS/CORS/metadata behavior.
- Local-filesystem storage is absent; private S3-compatible storage is required.
- A separate service is required; the Moodle ZIP does not provision Linux services.
- Native installer requires a clean dedicated host and refuses existing unowned DBs;
  automatic native changed-source upgrades are not implemented.
- TLS routing, object-storage provisioning, monitoring/backups and capacity sizing
  are operator responsibilities. MinIO/server images are not bundled.
- Security contact remains the owner's approved temporary address in SECURITY.md.
- Full normal cron/long-retention scheduling was not requalified in the focused
  RC2 run; the renamed task registered with faildelay 0.
- One unattributed non-HTTP blob lookup reported ERR_FILE_NOT_FOUND. Actual HLS
  playback, dimensions and seeking passed, with no HTTP failures or page exceptions
  in that check. This remains a non-blocking observation, not a claimed fix.

The unreleased [watch-progress follow-up plan](development/installation-ux/watch-progress-plan.md)
records a separate unresolved observation:
the ARM64 tester observed about 81% credit while backgrounded, then persisted
100% after visible replay. Cause is not established; no watch-credit code changed.
Installation-experience dev.3 has focused tests, not a new broad media matrix.

See the [RC2 release](https://github.com/abubakarmeraj/moodle-videolesson-stream/releases/tag/v3.1.0-rc2)
for the exact immutable distributions and accepted scope. Earlier Local-stage
qualification stamps in the frozen source/packages are historical; they were
not rewritten to produce different archive bytes.
