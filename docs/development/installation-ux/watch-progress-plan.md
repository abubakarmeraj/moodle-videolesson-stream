# Controlled visible/background watch-credit investigation (not a fix)

Observation supplied by the independent ARM64 tester: first background playback
16.242/20 seconds credited (~81.21%), an uncredited interval approximately
6.3109–10.068563 seconds; visible replay reached/persisted 100%. Browser throttling
is only a hypothesis. No watch/grant/completion implementation changes here.

Use an authorized disposable test site, one short synthetic source/revision,
same enrolled student policy, fixed speed 1× and fresh independent watch sessions.
Run at least three samples per case, preserving accepted ranges before/after:

1. Foreground visible, no seeks.
2. Same browser/window size, background tab for a fixed middle interval.
3. Visible but temporary controlled network interruption at that interval.

Record monotonic browser timestamps, media currentTime, visibility transitions,
play/pause/waiting/seeking/ratechange, event dispatch/send/receipt/ack timing,
server-accepted sequence/ranges, renewals and reload/reconnect results. Correlate
the missing interval with delivery and the intended trusted-watch credit limits;
do not infer credit from currentTime alone. Compare accepted sequence with lost
request/response cases without logging grant/token/cookie/user data.

No scripted completion, direct SQL repair, new event sequences to fabricate credit
or weakening of server wall-time/seek/auth checks. Separate intended policy from
transport/lifecycle defects. A separately authorized tester may execute this plan;
this phase only documents it.
