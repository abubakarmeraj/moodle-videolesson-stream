# RC1 to RC2: breaking prerelease identity transition

RC1 was published as `mod_videolesson`; RC2 is the distinct
`mod_videolessonstream` activity. Installing RC2 is **not** an in-place Moodle
upgrade. Moodle does not retag existing activities, capabilities, files, watch
progress or backup identifiers automatically. RC2's upgrade callback touches
only its own savepoint; it never claims RC1 tables or configuration.

A correct migration must coordinate module IDs, course-module instance IDs,
capabilities/role overrides, file-component contexts, completion/progress,
backup identities, durable provisioning intents and service reference generations.
That is not a cheap rename. No automatic migration tool is shipped in RC2.

Keep RC1 installed and its matched DB/moodledata/service/object backups intact
until a separately reviewed migration plan exists. **Do not uninstall RC1, rename
its tables, copy UUIDs into new activity rows or delete its media to switch.**
Fresh RC2 installations get their own plugin tables/config and a new protected
service tenant/state. Do not point two independent Moodle reference authorities
at the same writable service tenant. The service's reference snapshots are
whole authoritative sets, not a union across plugins/sites.

The RC2 service temporarily accepts authenticated protocol1 requests/old media
audiences when `SERVICE_ALLOW_LEGACY_PROTOCOL=true` (default). New RC2 requests
use protocol2. This wire alias is **not** a database/reference migration.
RC1 Test Connection still reports the newer tuple as untested. Preserve an
existing explicit Redis namespace when upgrading an isolated service; changing
the new default does not migrate pending queues. Preserve grant/subject/tenant
keys and database state. Disable legacy protocol only after old clients/grants
are retired. Ready media bytes, storage keys and migrations001–005 are unchanged.

RC1's immutable tag, release artifacts and historical manifests remain available
as provenance. The exact RC2 distributions passed focused Deployment qualification;
see the [RC2 prerelease](https://github.com/abubakarmeraj/moodle-videolesson-stream/releases/tag/v3.1.0-rc2)
for its scope. No automatic RC1 activity/data/media migration is supplied.
