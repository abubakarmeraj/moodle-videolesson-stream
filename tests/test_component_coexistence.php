<?php
// SPDX-License-Identifier: GPL-3.0-or-later
// Copyright 2026 ValeLMS contributors.
// Explicit disposable Moodle with the public RC1 predecessor fixture, not every upstream release.
define('CLI_SCRIPT', true);
if ($argc !== 2 || !is_file($argv[1])) {
    exit(2);
}
require($argv[1]);
require_once($CFG->dirroot . '/mod/videolesson/lib.php');
require_once($CFG->dirroot . '/mod/videolessonstream/lib.php');
$out = [];
function coexist($condition, $name) {
    global $out;
    if (!$condition) {
        throw new coding_exception('Coexistence failed: ' . $name);
    }
    $out[$name] = 'PASS';
}
$manager = core_plugin_manager::instance();
foreach (['videolesson' => 2026100701, 'videolessonstream' => 2026100702] as $module => $version) {
    coexist($manager->get_plugin_info('mod_' . $module) !== null, $module . '_discovery');
    coexist((int)get_config('mod_' . $module, 'version') === $version, $module . '_version');
    coexist($DB->record_exists('modules', ['name' => $module]), $module . '_registration');
    $xml = new xmldb_file($CFG->dirroot . '/mod/' . $module . '/db/install.xml');
    coexist($xml->loadXMLStructure(), $module . '_xmldb');
    foreach ($xml->getStructure()->getTables() as $table) {
        coexist($DB->get_manager()->table_exists($table), 'table_' . $table->getName());
    }
    coexist($DB->count_records('capabilities', ['component' => 'mod_' . $module]) === 4, $module . '_capabilities');
    set_config('rc2coexistenceprobe', $module, 'mod_' . $module);
}
coexist(get_config('mod_videolesson', 'rc2coexistenceprobe') === 'videolesson' &&
    get_config('mod_videolessonstream', 'rc2coexistenceprobe') === 'videolessonstream', 'config_isolation');
unset_config('rc2coexistenceprobe', 'mod_videolesson');
unset_config('rc2coexistenceprobe', 'mod_videolessonstream');
coexist(function_exists('videolesson_add_instance') && function_exists('videolessonstream_add_instance'), 'callbacks_isolation');
coexist(class_exists('\\mod_videolesson\\local\\providers') && class_exists('\\mod_videolessonstream\\local\\providers'), 'autoload_isolation');
coexist(\core\task\manager::get_scheduled_task('\\mod_videolesson\\task\\reconcile') !== null &&
    \core\task\manager::get_scheduled_task('\\mod_videolessonstream\\task\\reconcile') !== null, 'task_isolation');
$out['fixture_scope'] = 'Published GPL RC1 predecessor, not independently verified pristine upstream';
echo json_encode($out, JSON_PRETTY_PRINT), "\n";
