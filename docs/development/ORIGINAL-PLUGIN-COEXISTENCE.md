# Original-plugin coexistence boundary

RC2 is `mod_videolessonstream`, module/directory `videolessonstream`. It is
distinct from the upstream `mod_videolesson` and the RC1 predecessor fork.

| Boundary | RC2 isolation |
|---|---|
| Component/module registration | `mod_videolessonstream` / `videolessonstream` |
| Main table | `videolessonstream` |
| Other tables | `videolessonstream_*`; bounded `vls_data_external`, `vls_cm_progress`, `vls_folder_items` |
| Capabilities | `mod/videolessonstream:*` |
| PHP/autoload | `mod_videolessonstream\\*`; callbacks `videolessonstream_*` |
| Language | `lang/en/videolessonstream.php`, component-scoped strings |
| Config/cache/locks | `mod_videolessonstream`; `$CFG->videolessonstream_*` |
| File areas | intro/thumbnail are scoped by component+context; no original file adoption |
| Tasks/events/privacy/completion | new component class namespace |
| AMD | `mod_videolessonstream/*`; all source/build/maps regenerated |
| Templates/pix/DOM hooks | component-scoped templates/pix; `vls-*` player/upload hooks |
| Backup/restore | `backup_videolessonstream_*`, `restore_videolessonstream_*`; own XML/data mapping |
| URLs/admin nodes/web services | `/mod/videolessonstream/`; renamed settings/service identifiers |

All13 tables are distinct from RC1's tables, all names at most28 characters
(stricter than the tested Moodle5.2 XMLDB limit). Internal foreign keys and DML
use the matching table map. Core tables are unchanged.

Native disposable Moodle installation/discovery and coexistence passed for both
components simultaneously: all26 tables, four capabilities per component,
registration/version/config isolation, PHP callbacks/autoload and scheduled
tasks. RC1 fixture bytes remained identical after installation. RC1's GPL public
ZIP is a predecessor fixture, not proof of every unmodified upstream release.
No separately verified pristine original package is supplied by this project.
Deployment should qualify original-plugin coexistence if that private fixture is
available; it must not redistribute an unreviewed fixture.

Service storage/Redis/schema identifiers are not Moodle component tables. Separate
tenants/state and reference authorities are required; simply using different
module names does not make sharing one writable service tenant safe. See the
[RC1 transition](../rc1-to-rc2.md). No destructive migration/uninstall is performed.
