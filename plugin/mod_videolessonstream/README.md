# ValeLMS Video Lesson Stream 3.1.0

Moodle activity `mod_videolessonstream`, version2026101201; targets Moodle5.2.
Install the ZIP through Moodle's normal plugin installation workflow.

A separately deployed Video Service **0.5.0** is required. The Moodle ZIP
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
installation and the exact qualification boundary. This is the prepared stable
candidate; publication awaits final artifact verification and human approval.
Legacy vendor/AWS setup paths are unsupported. RC1 component/data migration is
not automatic; see the repository's docs/rc1-to-rc2.md before changing RC1.
