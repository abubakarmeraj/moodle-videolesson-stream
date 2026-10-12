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
 * Plugin upgrade steps are defined here.
 *
 * @package    mod_videolessonstream
 * @author     BitKea Technologies LLP
 * @copyright  2022-2026 BitKea Technologies LLP
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

defined('MOODLE_INTERNAL') || die();
/** The distinct component starts with RC2's complete install.xml schema. */
function xmldb_videolessonstream_upgrade($oldversion) {
    if ($oldversion < 2026100702) {
        upgrade_mod_savepoint(true, 2026100702, 'videolessonstream');
    }
    // Never claim, rename, read or drop another component's RC1 tables here.
    if ($oldversion < 2026101200) {
        // Installation guidance and uploader diagnostics only; no schema/data changes.
        upgrade_mod_savepoint(true, 2026101200, 'videolessonstream');
    }
    return true;
}
