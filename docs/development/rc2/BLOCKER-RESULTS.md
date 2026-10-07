# RC2 Local — blocked by Moodle activity-name architecture

Result: **NO-GO pending owner-approved technical component name**.
The requested `mod_videolesson_stream` cannot be installed by unmodified Moodle.
No RC2 artifact, tag, commit, push, remote rename or publication was performed.
Uncommitted work is retained on `codex/valelms-stream-rc2` as a draft, not accepted
product source. Generated current RC2 manifests are provisional snapshots only.

## Immutable baseline

Starting HEAD770fc98b789abfcbf56eb3d26fddbf8b615ec4c9/main is a README-only
successor to the published RC1 tag. `v3.1.0-rc1` resolves to
3c2f59f704421f199033f020fd60eec50ea84a8d. Packaged source commit was
bd41c0bd529848d2da10d105dd3dd74f109d5050. GitHub release is a prerelease.
Read-only GitHub asset digest metadata agrees with the independently hashed local
immutable archives:

- mod_videolesson-3.1.0-rc1.zip,763073bytes:
  0a1168c3ad40a4aabf4b166d85ad9a6e4945dac765959cb1107eec7b6c1622a0.
- codefortex-video-service-0.5.0-rc1.tar.gz,134110bytes:
  fbf2e5c250d4dba47cc64867988c13ad61d8c92d73c1ff2dd28ce97d650b7802.

RC1 manifests were copied byte-for-byte from the published tag into
docs/release/rc1; historical reports and notices were preserved, not overwritten.

## Architectural evidence

Fresh isolated Moodle5.2.2(Build20260810), core commit
acfa383c13dd46c83ca82894a8e95fac273fda33, MariaDB-backed new database/new
moodledata/new cloned application tree. No existing LMS HTTP or database
connection was used. Only the independent project-owned WSL development distro
was started; Golden LMS and Docker Desktop were untouched.

Actual `public/lib/classes/component.php:1530` implements
`core_component::is_valid_plugin_name()` specially for type `mod`:

```php
preg_match('/^[a-z][a-z0-9]*$/', $pluginname)
```

The source comment explicitly states underscores are forbidden in module names.
Discovery at line1063 skips invalid names. The candidate directory and version
file existed at the correct public/mod path. Cache purge and supported CLI
upgrade did not discover/register/install it; the native assertion failed on
the installed-version check, before any module data mutation.

The targeted native probe proves `videolesson_stream` invalid, while
`videolessonstream` satisfies the core validator. The requested component is
absent from discovery/module registration; its main table is absent.
The official [Moodle5.2 plugin-type documentation](https://moodledev.io/docs/5.2/apis/plugintypes)
also documents the activity-module underscore exception.

Raw private evidence: `.lab/evidence/development/rc2-identity/` contains the
name probe, failed native install/check logs, baseline/occurrence/table-map
inventories. No secrets are placed in public reports. Private test configuration
is outside the public tree. Core tracked source remains unchanged.

## Work completed before blocker

Draft plugin identity2026100702/ValeLMS3.1.0-rc2; service0.5.0-rc2;
protocol2 with exact-route X-VL HMAC headers and neutral media audience.
Explicit operator-disableable protocol1 compatibility retains replay protection.
Distinct13-table schema, capabilities, PHP callbacks/autoload, language,
templates/tasks/settings/URLs, backup and AMD source/build/map rename prepared.
No service migration006: migrations001–005 unchanged. No automatic RC1 data
migration is shipped; data/reference/file/completion migration is a separate
reviewed project, not an in-place rename. R2 first-class documentation added.

31 fast Python tests passed, covering configuration/S3/R2/SigV4, readiness,
protocol authentication/replay/alias negatives, tables/maps, metadata/artwork/
notices/installer guard. Ten compiled-uploader URL-security cases passed.
These do **not** prove Moodle component installation. Full release checks,
runtime coexistence, setup connection and final reproducible packaging are not
complete and are not claimed. Early failed intermediate tests remain private.

## Required owner decision

Recommended component **`mod_videolessonstream`**, directory
**`videolessonstream`**, while keeping public brand **ValeLMS Video Lesson Stream**
and planned repository **moodle-videolesson-stream**. Only the underscore inside
the module name must go; the Frankenstyle `mod_` separator remains.

This alternative has only been name-validated, not implemented/installed.
Do not bypass the validator or modify Moodle core. After owner approval,
finish coherent namespace/table/build changes, native install/coexistence,
fast checks/classified scans, final manifests, deterministic private archives
and the bounded Deployment handoff. Never publish or discard RC1 automatically.
