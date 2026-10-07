# Publication boundary

The current RC2 candidate is the owner-approved distinct activity plus reviewed
public source/deployment metadata; it is not yet authorized for publication.
Historical RC1 publication boundaries remain under rc1/. `git ls-files` is
the definitive committed-path inventory; docs/release/PUBLIC-SOURCE-MANIFEST.json
fingerprints all public files except itself. Product/service manifests and
IDENTITY.json identify release inputs. The build checks this boundary and rejects
untracked/uncommitted public source changes. Artifacts/checksums/evidence stay ignored.

| Paths | Classification | Rule |
|---|---|---|
| plugin/mod_videolessonstream (supported source/assets/builds) | PUBLIC_SOURCE | Exclude nested historical workflows, EVENT_FLOW_DOCUMENTATION.md, upgrade_comp.md |
| service/video-service | PUBLIC_SOURCE | Source, locked requirements, metadata, migrations; no runtime/cache/venv |
| deploy | PUBLIC_DEPLOYMENT | Portable installers/Compose and example-only policy; no completed secret config |
| tests/test_*.py, tests/test_upload_urls.cjs, tests/test_*.php | PUBLIC_TESTS | Synthetic/offline or explicit disposable Moodle input; no historical lab credentials |
| scripts/public_release.py, check_release.py, check_identity.py, render_artwork.py, build_upload_amd.cjs, scripts/amd manifests | PUBLIC_SOURCE | Build/check tooling; historical one-shot RC1 preparation script removed; node_modules ignored |
| Root README/CHANGELOG/SECURITY/CONTRIBUTING/CODE_OF_CONDUCT; public docs/*.md; selected docs/development audits/handoff and rc1 report/inventory; docs/release | PUBLIC_DOCS | No private phase transcripts/workstation paths |
| LICENSE, component licenses, THIRD_PARTY_NOTICES.md, docs/licenses, resource notices | PUBLIC_LICENSES | Upstream text preserved; project GPL3-or-later |
| .github/README.md, issue forms, PR template, read-only fast-check workflow; .gitignore, .gitattributes, .dockerignore | PUBLIC_COMMUNITY | No deployment/publishing workflow; no secrets; public PR contribution path |
| .lab/evidence, historical docs/deployment, other docs/development | PRIVATE_DEV_EVIDENCE | Retained locally, ignored, not packaged |
| .lab/secrets, generated env/keys/connection handoffs | PRIVATE_SECRETS | Never commit/package |
| .lab/work, .lab/fixtures, .lab/releases, DB/WSL/VM/browser/media state | PRIVATE_RUNTIME | Ignored, not part of product |
| scripts/os*, scripts/final_qualification*, old lab-specific PHP fixtures, obsolete plugin docs/workflows | NOT_FOR_PUBLICATION | Preserved historical tooling, ignored; not current install commands |

No private historical files are moved/deleted to make the public surface look clean.
The old inherited artwork is replaced at its stable source paths and cannot enter
the initial public history. .gitignore excludes private data but does not exclude
current source manifests, notices, public tests or required examples. Public text
scans and normalized archive inventory checks supplement, not replace, review.

Immutable RC1 archives/tag/releases are not rebuilt or relabeled. New RC2 archive
embedded manifests identify the exact clean source commit and public source
manifest hash. Qualification candidates remain private until Deployment review
and separate publication authorization. SECURITY.md retains the owner-approved
temporary contact; it is not replaced with an unconfirmed mailbox.
