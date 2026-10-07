<?php
// ValeLMS local test gateway, GPL v3 or later. A real provider uses its own gateway.
require(__DIR__ . '/../../config.php');
$cmid = required_param('id', PARAM_INT);
[, , , $instance] = \mod_videolessonstream\local\access::activity($cmid);
if (empty($CFG->videolessonstream_test_mode) || $instance->tenantid !== \mod_videolessonstream\local\providers::tenant()) {
    throw new moodle_exception('cfproviderunavailable', 'mod_videolessonstream');
}
$provider = \mod_videolessonstream\local\providers::get();
if (!$provider instanceof videolessonstream_test_provider) {
    throw new moodle_exception('cfproviderunavailable', 'mod_videolessonstream');
}
$grant = required_param('grant', PARAM_RAW);
$file = required_param('file', PARAM_RAW);
$path = $provider->asset($instance->tenantid, $instance->videouuid, (int)$instance->mediarevision,
    (int)$USER->id, $grant, $file);
\core\session\manager::write_close();
header('Cache-Control: private, no-store');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: no-referrer');
if (str_ends_with($file, '.m3u8')) {
    header('Content-Type: application/vnd.apple.mpegurl');
    $directory = dirname($file);
    $playlist = file($path, FILE_IGNORE_NEW_LINES);
    foreach ($playlist as $line) {
        if ($line !== '' && $line[0] !== '#') {
            $child = ($directory === '.' ? '' : $directory . '/') . $line;
            // Validate each resolved segment/playlist before returning its URL.
            $provider->asset($instance->tenantid, $instance->videouuid, (int)$instance->mediarevision,
                (int)$USER->id, $grant, $child);
            $line = (new moodle_url('/mod/videolessonstream/media.php',
                ['id' => $cmid, 'grant' => $grant, 'file' => $child]))->out(false);
        }
        echo $line . "\n";
    }
} else {
    $mime = str_ends_with($file, '.ts') ? 'video/mp2t' : 'video/mp4';
    send_file($path, basename($file), 0, 0, false, false, $mime);
}
