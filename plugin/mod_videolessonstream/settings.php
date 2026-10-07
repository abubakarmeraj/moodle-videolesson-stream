<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Moodle is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Moodle.  If not, see <http://www.gnu.org/licenses/>.

/**
 * Settings
 *
 * @package    mod_videolessonstream
 * @author     BitKea Technologies LLP
 * @copyright  2022-2026 BitKea Technologies LLP
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

defined('MOODLE_INTERNAL') || die();
$ADMIN->add('modsettings', new admin_externalpage('videolessonstreamservice',
    get_string('cfservicesetup', 'mod_videolessonstream'), new moodle_url('/mod/videolessonstream/service_setup.php'), 'moodle/site:config'));
$ADMIN->add('modsettings', new admin_externalpage('videolessonstreamstorage',
    get_string('cfstorage', 'mod_videolessonstream'), new moodle_url('/mod/videolessonstream/storage.php'), 'moodle/site:config'));
if ($ADMIN->fulltree) {
    $settings->add(new \mod_videolessonstream\local\quota_setting('mod_videolessonstream/storagequotamib',
        get_string('cfstoragequota', 'mod_videolessonstream'), get_string('cfstoragequotadesc', 'mod_videolessonstream'), 0, PARAM_RAW));
    $settings->add(new admin_setting_configselect('mod_videolessonstream/recoverydays',
        get_string('cfrecoverydays', 'mod_videolessonstream'), get_string('cfrecoverydesc', 'mod_videolessonstream'),
        7, array_combine([0, 1, 3, 7, 14, 30], [0, 1, 3, 7, 14, 30])));
    $settings->add(new \mod_videolessonstream\local\upload_limit_setting('mod_videolessonstream/maxuploadmib',
        get_string('cfmaxupload', 'mod_videolessonstream'), get_string('cfmaxuploaddescription', 'mod_videolessonstream'),
        '512', PARAM_RAW));
    $settings->add(new admin_setting_heading('mod_videolessonstream/cfprovider',
        get_string('pluginname', 'mod_videolessonstream'), get_string('cfproviderdescription', 'mod_videolessonstream')));
    $settings->add(new admin_setting_configselect('mod_videolessonstream/encodingprofile',
        get_string('cfencodingprofile', 'mod_videolessonstream'), get_string('cfencodingdescription', 'mod_videolessonstream'),
        'standard', ['economy' => 'Economy (480p)', 'standard' => 'Standard (480p + 720p)',
            'full' => 'Full (480p + 720p + 1080p)']));
    $settings->add(new admin_setting_heading('mod_videolessonstream/neverupscale',
        get_string('cfneverupscale', 'mod_videolessonstream'), get_string('cfneverupscaledescription', 'mod_videolessonstream')));
    $settings->add(new admin_setting_configselect('mod_videolessonstream/hlssegmentseconds',
        get_string('cfhlssegment', 'mod_videolessonstream'), get_string('cfhlssegmentdescription', 'mod_videolessonstream'),
        4, [2 => '2', 4 => '4', 6 => '6']));
    $settings->add(new admin_setting_configselect('mod_videolessonstream/rawretentiondays',
        get_string('cfrawretention', 'mod_videolessonstream'), get_string('cfrawretentiondescription', 'mod_videolessonstream'), 1, [1 => '1']));
}
