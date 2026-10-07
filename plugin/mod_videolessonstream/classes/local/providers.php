<?php
// ValeLMS contributors additions, GPL v3 or later.
namespace mod_videolessonstream\local;
defined('MOODLE_INTERNAL') || die();

final class providers {
    public static function get(): provider {
        global $CFG;
        if (service_setup::configuration()) { return new real_provider(); }
        // Test implementation is outside deployable plugin source. Production has no fake fallback.
        if (empty($CFG->videolessonstream_test_provider_file) || empty($CFG->videolessonstream_test_mode)) {
            throw new \moodle_exception('cfproviderunavailable', 'mod_videolessonstream');
        }
        require_once($CFG->videolessonstream_test_provider_file);
        return new \videolessonstream_test_provider();
    }

    public static function tenant(): string {
        global $CFG;
        $tenant = service_setup::configuration()['tenant'] ?? $CFG->videolessonstream_tenant ?? '';
        if (!preg_match('/^[a-zA-Z0-9_-]{8,64}$/D', $tenant)) {
            throw new \moodle_exception('cfproviderunavailable', 'mod_videolessonstream');
        }
        return $tenant;
    }

    public static function media(\stdClass $instance): array {
        if (empty($instance->trustedref) || empty($instance->videouuid) || $instance->tenantid !== self::tenant()) {
            throw new \moodle_exception('cfrelink', 'mod_videolessonstream');
        }
        $media = self::get()->get_video($instance->tenantid, $instance->videouuid);
        if ($media['state'] !== 'ready' || $media['revision'] !== (int)$instance->mediarevision ||
                !is_numeric($media['duration']) || $media['duration'] <= 0 || $media['duration'] > service_setup::MAX_DURATION) {
            throw new \moodle_exception('cfnotready', 'mod_videolessonstream');
        }
        return $media;
    }
}
