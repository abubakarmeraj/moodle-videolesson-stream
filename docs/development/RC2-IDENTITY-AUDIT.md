# RC2 identity and branding audit

Owner decisions: ValeLMS Video Lesson Stream; `mod_videolessonstream`;
plugin2026100702 / ValeLMS3.1.0-rc2; service0.5.0-rc2, protocol2. Future repository
name `moodle-videolesson-stream`; remote rename/publication is not performed here.

The owner explicitly approved the no-internal-underscore spelling after native
Moodle rejected the original request. `mod_videolesson_stream` is retained only
in historical blocker evidence and a negative validation test. The release guard
and identity validator require Moodle's activity-name grammar, not just a path rename.

The before/after occurrence inventories in `rc2/IDENTITY-OCCURRENCES.json` record
every case-insensitive old-brand hit by path/line/column/classification. The
before inventory covers starting tracked source, including historical manifests;
the after inventory covers the intended candidate tree, including preserved RC1
metadata. These scopes differ because historical copies are added deliberately.
Generated inventories themselves are excluded from recursive occurrence counting.

| Class | Treatment |
|---|---|
| A PUBLIC BRANDING | Current product display/docs/output use ValeLMS; ordinary UI remains clear Video/Upload/Status terminology |
| B PROJECT-OWNED NOTICE | Owner-authorized new notices use ValeLMS contributors; RC1 copies remain historical |
| C PACKAGE/RUNTIME NAME | player→stream_player, controls→videolesson-controls, test provider→videolessonstream_test_provider; package/image valelms-video-service |
| D PERSISTED IDENTIFIER | Fresh activity source is service; independent component/config/tables; new neutral Redis default. Existing explicitly configured namespaces are not rewritten |
| E WIRE IDENTIFIER | New `/v2/rpc`, X-VL headers and videolesson-stream-media audience; only explicit, operator-disableable protocol1 aliases/tests remain |
| F HISTORICAL PROVENANCE | Immutable RC1 reports/tag/artifacts/manifests and original-component/migration/collision notes; not current executable identity |
| G THIRD-PARTY TEXT | All upstream notices/grants and bundled dependency bytes preserved; no CodeFortex third-party ownership asserted |

No global branding replacement was applied to third-party bundles/licenses or
historical RC1 reports/manifests. A classified mechanical identity map updated
component-owned PHP/DML/JS/template/settings references, followed by AMD rebuild
and actual native Moodle installation tests. The explicit13-table map uses
bounded names and rewires internal keys/queries. Inherited RC1 upgrade steps are
not a valid migration into this distinct module and are not shipped as such.
Full old/new path/hash delta is in `rc2/RC1-DELTA.json`.

## Protocol boundary

Protocol2 signs POST + exact `/v2/rpc` + key ID + timestamp + nonce + SHA256(body)
with the unchanged HMAC-SHA256 algorithm. Header family is X-VL-Key/Time/Nonce/
Signature. Duplicate and mixed families are rejected. Shared nonce storage rejects
replay even across protocol families. Time/key expiry and bounded ingress remain.
New grants use `videolesson-stream-media`. When
`SERVICE_ALLOW_LEGACY_PROTOCOL=true`, `/v1/rpc` accepts only its own X-CF header
family/canonical path and verifies signed `codefortex-media` grants until expiry.
The false setting denies both aliases. It never accepts unsigned compatibility.
No service schema change: migrations001–005 are byte-identical.

## Coexistence and migration

See [coexistence](ORIGINAL-PLUGIN-COEXISTENCE.md) and
[RC1 transition](../rc1-to-rc2.md). Separate writable reference authorities need
separate tenant/state. No automatic cross-component migration, original-plugin
uninstall, table adoption or media deletion is performed.

## Artwork / licensing

RC1 geometric SVG/PNG artwork is retained. Only current SVG title/notice text
changes and the controls filename is neutralized; no new graphic design.
GPL-3.0-or-later is unchanged. BitKea/MooPlugins/Moodle/dependency notices remain
unaltered. Security contact remains the owner's approved temporary Gmail address.
