# ValeLMS contributor / installation-agent router

Read README.md first. Installation agents use docs/ai-installation.md and the
same docs/quick-start.md and deploy/setup.py as human operators; no hidden installer.

Preserve existing applications/data. Do not regenerate an installed tenant or
subject key to retry startup. Never print credentials, connection JSON, cookies,
presigned URLs or raw provider error bodies. Do not disable TLS or access guards.
Network/write preflight probes need explicit operator selection and isolated keys.

Development: use scripts/check_release.py, tests/test_upload_errors.cjs and
tests/test_installation_ux.py. Rebuild AMD with scripts/build_upload_amd.cjs after
JS changes. Keep generated source maps and reviewed manifests in sync. Evidence
belongs under ignored .lab/evidence, not product source. Historical release tags,
assets and qualification reports are immutable. No publication without approval.

Published Stable/RC source tags and assets are immutable. Work on a new development
branch/version for future changes; never repack published assets from later main.
The release tag identifies qualified product source. Later documentation-only
publication commits must not change plugin/service/deploy/tooling payloads.
