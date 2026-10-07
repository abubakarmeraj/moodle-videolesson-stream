<?php
// SPDX-License-Identifier: GPL-3.0-or-later
// Copyright 2026 ValeLMS contributors. Explicit disposable-site setup smoke, not production.
define('CLI_SCRIPT', true);
if (!in_array($argc, [2, 3], true) || !is_file($argv[1])) {
    fwrite(STDERR, "Usage: php test_moodle_setup.php <disposable-moodle-config.php> [protected-test-handoff.json]\n");
    exit(2);
}
require($argv[1]);
require_once($CFG->libdir . '/adminlib.php');
\core\session\manager::set_user(get_admin());
if ($argc === 3) {
    $CFG->videolessonstream_connection_file = $argv[2];
}
$connection = (new \mod_videolessonstream\local\real_provider())->test_connection();
$out = ['connection_status' => $connection['connection_status'],
    'plugin_version' => get_config('mod_videolessonstream', 'version')];
echo json_encode($out), "\n";
exit($out['connection_status'] === 'COMPATIBLE' && $out['plugin_version'] == 2026100702 ? 0 : 1);
