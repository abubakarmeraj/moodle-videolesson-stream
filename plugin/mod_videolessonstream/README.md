# ValeLMS Video Lesson Stream 3.1.0-dev.3 (unreleased)

Moodle activity `mod_videolessonstream`, version2026101200; targets Moodle5.2.
Install the ZIP through Moodle's normal plugin installation workflow.

A separately deployed Video Service **0.5.0-rc2** is required. The Moodle ZIP
does not install Linux services or perform FFmpeg encoding in PHP.
Configure the protected six-field connection handoff using **Site administration
→ Plugins → Activity modules → Video Service configuration**, then Test Connection.

Teachers create a Video Lesson and upload directly to private S3-compatible
storage. Moodle owns enrolment/access, progress and completion. Administrator
policies control upload size, quota, recovery, renditions and HLS segments.
Video storage is a settings page within this plugin, not a separate plugin.

Project-owned code/artwork: GPL-3.0-or-later; upstream copyrights/licenses retained.
LICENSE and THIRD_PARTY_NOTICES.md are included in the release archive.
See the repository's docs/quick-start.md and docs/known-limitations.md for service
installation and the exact qualification boundary. This is development source,
not the immutable published RC2 ZIP or stable software. Legacy vendor/AWS setup paths are unsupported.
