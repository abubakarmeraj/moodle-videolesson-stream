# Upgrading to ValeLMS 3.1.0

Use the coordinated **plugin 2026101201 / ValeLMS 3.1.0 + service 0.5.0**
packages from the [Stable release](https://github.com/abubakarmeraj/moodle-videolesson-stream/releases/tag/v3.1.0).
The exact pair passed a supported RC2-to-Stable upgrade in an isolated matched
clone. Never manually patch or overwrite published RC1/RC2 assets. Keep matched
backups of Moodle DB/moodledata, service DB, protected
identity/configuration and storage before an approved upgrade.

From `mod_videolessonstream` RC2 (2026100702) or dev.3 (2026101200), normal Moodle
upgrade records the supported savepoint(s) through **2026101201**. No table,
column or data migration is introduced. Do not lower a recorded version. The
setup entry uses a normal empty Moodle config setting, not a schema table.

Service 0.5.0 changes release metadata only relative to the accepted 0.5.0-rc2
runtime; schema remains **001–005**, dependency lock unchanged, **no migration006**.
Replace the coordinated packages in one controlled maintenance window: gracefully
drain/stop old service roles, preserve tenant/subject/RPC/grant keys, DB/Redis
identity/namespace and explicit storage configuration, build the new local image,
then restart the same Compose project/config/port choices. Do not run setup.py
again to regenerate an existing installation. Native changed-source replacement
still needs its explicit upgrade procedure, not deletion/reinstall of the database.

Stable plugin Test Connection intentionally requires service **0.5.0 / protocol 2**;
an RC2-only service is SERVICE_TOO_OLD. Install the matched pair, not plugin-only.
Existing ready media, references and watch credit are not rewritten/retranscoded.
Purge Moodle caches, Test Connection, then a short upload/playback/completion smoke.
Do not treat this Local preparation as permission to modify a hosted site.

## Historical RC1 → RC2 identity boundary

RC2 coordinates **mod_videolessonstream2026100702 / ValeLMS3.1.0-rc2** with
**ValeLMS Video Service0.5.0-rc2**, protocol2/schema001–005. RC1 was a different
component, `mod_videolesson`. **Installing RC2 is not an in-place RC1 plugin
upgrade.** Read [RC1 to RC2](rc1-to-rc2.md) before changing an existing prerelease site.

Keep matched backups of Moodle DB/moodledata, service MariaDB, protected
configuration and both buckets. Do not uninstall RC1, rename/adopt its tables or
assume Moodle migrates activities/files/progress/capabilities automatically.
Fresh RC2 installs its own13-table namespace. It has only its own version savepoint;
there is no inherited RC1 upgrade chain or automatic destructive migration.

Service migrations001–005 and dependency lock are unchanged; no006 is introduced
for identity/protocol changes. Stop roles during controlled source replacement;
preserve DB/Redis identities, explicit Redis namespace, tenant, policy and secrets.
The new default namespace does not migrate old queues. Do not point separate
Moodle reference authorities at the same writable service tenant/state.

New requests sign the exact `/v2/rpc` route with X-VL headers; new grants use the
neutral media audience. Authenticated protocol1 aliases temporarily remain when
SERVICE_ALLOW_LEGACY_PROTOCOL=true. Disable them only after retiring old clients
and grants. Aliases do not migrate Moodle data; RC1's setup compatibility tuple
does not silently become RC2-compatible. Existing ready objects are not retranscoded.

Compose: use the new verified bundle and existing protected VIDEO_CONFIG for a
controlled service upgrade. Native: stop roles, prepare a verified release/venv
and explicitly switch current after matched backup; the installer deliberately
does not silently adopt changed source. Never regenerate identity as routine upgrade.

Purge Moodle caches normally after installing/replacing RC2 source. Require
Test Connection and a short matched-artifact upload/playback/completion smoke
before normal use. Do not bypass Moodle downgrade protection, publish RC2 or
modify an existing hosted LMS as part of Local qualification.
