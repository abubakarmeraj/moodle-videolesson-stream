<?php
// SPDX-License-Identifier: GPL-3.0-or-later
// Copyright 2026 ValeLMS contributors. Offline upgrade/onboarding assertions only.
define('MOODLE_INTERNAL', true);
define('MATURITY_STABLE', 200);
$plugin = new stdClass();
require(__DIR__ . '/../plugin/mod_videolessonstream/version.php');
$savepoints = [];
function upgrade_mod_savepoint($success, $version, $component) {
    global $savepoints;
    $savepoints[] = [$success, $version, $component];
}
require(__DIR__ . '/../plugin/mod_videolessonstream/db/upgrade.php');
xmldb_videolessonstream_upgrade(2026101200);
if ($savepoints !== [[true, 2026101201, 'videolessonstream']] || $plugin->version !== 2026101201) {
    throw new RuntimeException('Stable savepoint mismatch');
}
$savepoints = [];
xmldb_videolessonstream_upgrade(2026101201);
if ($savepoints) {
    throw new RuntimeException('Upgrade must be idempotent');
}
require(__DIR__ . '/../plugin/mod_videolessonstream/lang/en/videolessonstream.php');
foreach (['install', 'storage', 'handoff', 'test', 'smoke'] as $step) {
    if (empty($string['cfsetupstep_' . $step])) {
        throw new RuntimeException('Missing onboarding step');
    }
    if (empty($string['cfsetupguide_' . $step])) {
        throw new RuntimeException('Missing clickable guide label');
    }
}
$settings = file_get_contents(__DIR__ . '/../plugin/mod_videolessonstream/settings.php');
if (!str_contains($settings, "new admin_setting_configempty('mod_videolessonstream/setupsteps'") ||
        !str_contains($settings, "new moodle_url('/mod/videolessonstream/service_setup.php')")) {
    throw new RuntimeException('New settings must include a persistable empty setting, not an omitted heading');
}
$page = file_get_contents(__DIR__ . '/../plugin/mod_videolessonstream/service_setup.php');
if (!str_contains($page, "require_capability('moodle/site:config'") || !str_contains($page, 'require_sesskey()') ||
        !str_contains($page, "html_writer::start_tag('ol')")) {
    throw new RuntimeException('Onboarding/admin authorization contract changed');
}
foreach (['docker.md', 'storage.md', 'configuration.md', 'troubleshooting.md', 'quick-start.md'] as $guide) {
    if (!str_contains($page, "'" . $guide . "'") || !is_file(__DIR__ . '/../docs/' . $guide)) {
        throw new RuntimeException('Missing supported documentation target');
    }
}
if (!str_contains($page, "'rel' => 'noopener noreferrer'")) {
    throw new RuntimeException('Documentation links need safe new-tab attributes');
}
echo "INSTALLATION_GUIDANCE_AND_SAVEPOINT=PASS (offline, not a browser test)\n";
