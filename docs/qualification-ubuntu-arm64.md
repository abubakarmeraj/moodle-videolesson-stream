# Independent RC2 first-time installation: Ubuntu ARM64 (2026-10-12)

Separate evidence from earlier Ubuntu WSL2 qualification. The tester used the
**published RC2 artifacts unchanged**, not the installation-experience branch.
This summary is supplied evidence, not a new connection to that VM by Video Local.

| Item | Tested value |
|---|---|
| OS/architecture | Ubuntu 24.04.5, aarch64, ordinary VM |
| Moodle/PHP/DB | 5.2.4 Build 20261005 / 8.3.6 / MariaDB 10.11.14 |
| Resources | 2 CPUs, about 5.8 GiB RAM, no swap, about 44 GiB initial free disk |
| Runtime | Docker 29.9.0 / Compose 5.6.0; Video Service 0.5.0-rc2 |
| Storage | SeaweedFS 4.48, private raw/processed, HTTPS/exact-origin CORS |
| Plugin | mod_videolessonstream 2026100702 / ValeLMS 3.1.0-rc2 |
| Integrity | All 238 plugin / 106 service archive entries matched afterward |
| Workflow | Install, signed Test Connection, browser upload, processing, HLS playback, saved progress/completion passed |

20-second 640×360 H.264/AAC synthetic source: 1,883,563 bytes; decoded
640×360 HLS (no upscale), readyState 4, natural time 20.032 seconds. Initial
background run credited 16.242 seconds (~81.21%); visible replay filled watched
range [0,20], 20 seconds / 100%, completion 1 persisted. Cause of the initial gap
is **unproven**. [Follow-up plan](development/installation-ux/watch-progress-plan.md).

Installation friction was real: unavailable MinIO downloads, local-image pull
before build, API processed-bucket HEAD permission, SeaweedFS volume allocation
500 despite healthy HEAD, and storage failure mislabeled as pause. Same session
resumed after storage correction; no product-source modification was needed.

Measured report: **40m36s** including preservation/final checks; baseline to first
play **20m23s**; **33 remote shell submissions**, **15 authored files** (8 active,
6 unused MinIO, 1 diagnostic), **11 operator choices**, **6 documentation gaps**,
0 human prompts. These are not the new tooling's elapsed performance. No matched
timed second install has been performed. Protected backups were retained; whole
VM restore was not tested. Native/systemd, long endurance, multi-GiB and a new
cross-browser matrix are not established by this run.

The underlying report's digest is recorded in the local installation-UX evidence.
Private hostnames/IPs, paths, credential retrieval files and screenshots containing
host details are deliberately not copied into this public summary.
