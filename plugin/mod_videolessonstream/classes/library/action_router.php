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
 * Action router for library actions
 *
 * @package    mod_videolessonstream
 * @author     BitKea Technologies LLP
 * @copyright  2022-2026 BitKea Technologies LLP
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

namespace mod_videolessonstream\library;

/**
 * Routes actions to appropriate handler classes
 */
class action_router {
    /** @var array Map of action names to class names */
    private static $actions = [
        'upload' => 'mod_videolessonstream\library\action\upload',
        'delete' => 'mod_videolessonstream\library\action\delete',
        'retry' => 'mod_videolessonstream\library\action\retry',
        'instances' => 'mod_videolessonstream\library\action\instances',
        'list' => 'mod_videolessonstream\library\action\list_action',
    ];

    /**
     * Execute the specified action
     *
     * @param string $action Action name
     * @throws \moodle_exception If action not found
     */
    public static function execute($action) {
        $action = $action ?? 'list';

        if (!isset(self::$actions[$action])) {
            // Default to list if action not found.
            $action = 'list';
        }

        $classname = self::$actions[$action];
        if (!class_exists($classname)) {
            throw new \moodle_exception('error:action_not_found', 'mod_videolessonstream', null, $action);
        }

        $handler = new $classname();

        // Automatically setup navigation if method exists.
        if (method_exists($handler, 'setup_navigation')) {
            $handler->setup_navigation();
        }

        $handler->execute();
    }
}
