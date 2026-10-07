<?php
// SPDX-License-Identifier: GPL-3.0-or-later
// Copyright 2026 ValeLMS contributors.
// Explicit disposable Moodle test; no media/service/storage connection.
define('CLI_SCRIPT', true);
if ($argc !== 2 || !is_file($argv[1])) {
    fwrite(STDERR, "Usage: php test_component_install.php <disposable-moodle-config.php>\n");
    exit(2);
}
require($argv[1]);
require_once($CFG->libdir . '/adminlib.php');
require_once($CFG->dirroot . '/course/lib.php');
require_once($CFG->dirroot . '/course/modlib.php');
require_once($CFG->dirroot . '/backup/util/includes/backup_includes.php');
require_once($CFG->dirroot . '/backup/util/includes/restore_includes.php');
require_once($CFG->dirroot . '/backup/moodle2/backup_stepslib.php');
require_once($CFG->dirroot . '/backup/moodle2/restore_stepslib.php');
require_once($CFG->dirroot . '/backup/moodle2/backup_activity_task.class.php');
require_once($CFG->dirroot . '/backup/moodle2/restore_activity_task.class.php');
require_once($CFG->dirroot . '/mod/videolessonstream/lib.php');
\core\session\manager::set_user(get_admin());
$CFG->videolessonstream_tenant = 'rc2_disposable_tenant';
$out = [];
function assert_contract($condition, $name) {
    global $out;
    if (!$condition) {
        throw new coding_exception('Component contract failed: ' . $name);
    }
    $out[$name] = 'PASS';
}
assert_contract(get_config('mod_videolessonstream', 'version') == 2026100702, 'version');
$plugins = \core_component::get_plugin_list('mod');
assert_contract(isset($plugins['videolessonstream']), 'component_discovery');
$info = core_plugin_manager::instance()->get_plugin_info('mod_videolessonstream');
assert_contract($info && $info->component === 'mod_videolessonstream', 'component_identity');
$xml = new xmldb_file($CFG->dirroot . '/mod/videolessonstream/db/install.xml');
assert_contract($xml->loadXMLStructure(), 'xmldb_structure');
$table_names = [];
foreach ($xml->getStructure()->getTables() as $table) {
    assert_contract($DB->get_manager()->table_exists($table), 'table_' . $table->getName());
    $table_names[] = $table->getName();
}
$caps = $DB->get_records('capabilities', ['component' => 'mod_videolessonstream']);
assert_contract(count($caps) > 0 && count(array_filter($caps,
    fn($c) => str_starts_with($c->name, 'mod/videolessonstream:'))) === count($caps), 'capabilities');
assert_contract(\core\task\manager::get_scheduled_task('\\mod_videolessonstream\\task\\reconcile') !== null, 'scheduled_task');
$admin = admin_get_root(true, true);
assert_contract($admin->locate('videolessonstreamservice') !== false &&
    $admin->locate('videolessonstreamstorage') !== false, 'admin_pages');
assert_contract(get_string('pluginname', 'mod_videolessonstream') === 'ValeLMS Video Lesson Stream', 'language');
foreach (['backup_videolessonstream_activity_task', 'restore_videolessonstream_activity_task'] as $classname) {
    $kind = str_starts_with($classname, 'backup_') ? 'backup' : 'restore';
    require_once($CFG->dirroot . '/mod/videolessonstream/backup/moodle2/' . $classname . '.class.php');
    assert_contract(class_exists($classname), $kind . '_class');
}
assert_contract(class_exists('\\mod_videolessonstream\\completion\\custom_completion') &&
    class_exists('\\mod_videolessonstream\\privacy\\provider') &&
    class_exists('\\mod_videolessonstream\\event\\course_module_viewed'), 'autoload_subsystems');
$rendered = $OUTPUT->render_from_template('mod_videolessonstream/stream_player', ['name' => 'RC2 native contract']);
assert_contract(str_contains($rendered, 'id="vls-player"'), 'template_resolution');
foreach (['stream_player', 'upload', 'constants'] as $module) {
    $PAGE->requires->js_call_amd('mod_videolessonstream/' . $module, 'init', [[]]);
    assert_contract(is_file($CFG->dirroot . '/mod/videolessonstream/amd/build/' . $module . '.min.js'), 'amd_' . $module);
}
$course = create_course((object)['fullname' => 'RC2 component contract',
    'shortname' => 'RC2-' . bin2hex(random_bytes(4)), 'category' => 1]);
$data = (object)['course' => $course->id, 'name' => 'Stream contract activity',
    'modulename' => 'videolessonstream', 'module' => $DB->get_field('modules', 'id', ['name' => 'videolessonstream']),
    'section' => 0, 'visible' => 1, 'intro' => '', 'introformat' => FORMAT_HTML,
    'mediakind' => 'hls', 'cfsubmission' => bin2hex(random_bytes(32)), 'cmidnumber' => '', 'completion' => 0];
$created = add_moduleinfo($data, $course);
assert_contract($DB->record_exists('videolessonstream', ['id' => $created->instance]), 'native_add_activity');
assert_contract($DB->record_exists('videolessonstream_intent', ['instanceid' => $created->instance]), 'durable_pending_intent');
assert_contract($DB->get_field('modules', 'name', ['id' => $created->module]) === 'videolessonstream', 'native_module_registration');
$out['tables'] = $table_names;
$out['capability_count'] = count($caps);
$out['original_component_present'] = isset($plugins['videolesson']);
echo json_encode($out, JSON_PRETTY_PRINT), "\n";
