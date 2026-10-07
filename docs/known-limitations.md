# Known qualification limits

- RC1 is a published prerelease. RC2 is a private qualification candidate, not stable
  software or an automatic in-place RC1 migration.
- Ubuntu24.04 under WSL2 is qualified; an ordinary Ubuntu VM/server run is pending.
- RC2 Local fresh discovery/install and signed setup passed on Moodle5.2.2/PHP8.3.6.
  Short synthetic-media lifecycle evidence below belongs to RC1 until Deployment
  qualifies the matched RC2 artifacts.
- Chromium completed generic-S3 multipart upload; Firefox/WebKit decoded playback
  and seeking passed, but their multipart upload was not separately repeated.
- Six-hour endurance, multi-GiB stress and full-disk endurance are not qualified.
- Generic S3 compatibility depends on the actual provider's TLS/CORS/metadata behavior.
- Local-filesystem storage is absent; private S3-compatible storage is required.
- A separate service is required; the Moodle ZIP does not provision Linux services.
- Native installer requires a clean dedicated host and refuses existing unowned DBs;
  automatic native changed-source upgrades are not implemented.
- TLS routing, object-storage provisioning, monitoring/backups and capacity sizing
  are operator responsibilities. MinIO/server images are not bundled.
- Security contact remains the owner's approved temporary address in SECURITY.md.

These are honest boundaries, not newly discovered defects. Source preparation
does not replace the focused RC2 Deployment smoke or publication approval.
