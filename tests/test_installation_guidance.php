<?php
// SPDX-License-Identifier: GPL-3.0-or-later
// Copyright 2026 ValeLMS contributors. Offline upgrade/onboarding assertions only.
define('MOODLE_INTERNAL', true);
define('MATURITY_ALPHA', 50);
$plugin = new stdClass();
require(__DIR__ . '/../plugin/mod_videolessonstream/version.php');
$savepoints = [];
function upgrade_mod_savepoint($success, $version, $component) {
    global $savepoints;
    $savepoints[] = [$success, $version, $component];
}
require(__DIR__ . '/../plugin/mod_videolessonstream/db/upgrade.php');
xmldb_videolessonstream_upgrade(2026100702);
if ($savepoints !== [[true, 2026101200, 'videolessonstream']] || $plugin->version !== 2026101200) {
    throw new RuntimeException('Development savepoint mismatch');
}
$savepoints = [];
xmldb_videolessonstream_upgrade(2026101200);
if ($savepoints) {
    throw new RuntimeException('Upgrade must be idempotent');
}
require(__DIR__ . '/../plugin/mod_videolessonstream/lang/en/videolessonstream.php');
foreach (['install', 'storage', 'handoff', 'test', 'smoke'] as $step) {
    if (empty($string['cfsetupstep_' . $step])) {
        throw new RuntimeException('Missing onboarding step');
    }
}
$page = file_get_contents(__DIR__ . '/../plugin/mod_videolessonstream/service_setup.php');
if (!str_contains($page, "require_capability('moodle/site:config'") || !str_contains($page, 'require_sesskey()') ||
        !str_contains($page, "html_writer::start_tag('ol')")) {
    throw new RuntimeException('Onboarding/admin authorization contract changed');
}
echo "INSTALLATION_GUIDANCE_AND_SAVEPOINT=PASS (offline, not a browser test)\n";
