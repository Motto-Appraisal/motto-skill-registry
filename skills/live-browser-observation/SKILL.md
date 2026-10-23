---
name: live-browser-observation
description: Let the user shadow real browser automation continuously in Factory's native browser side panel. Reuse the existing observable session, prefer attaching the user's working browser, and use agent-browser live streaming without HTML wrappers, screenshot feeds, or routine image files.
version: 1.2.0
compatibility: droid
---

# Live browser observation

The user wants to watch the browser you are actually working in. Start doing
the real task in the observable session. Do not substitute a demo page, a
pretty dashboard, a recording, or a sequence of screenshot files.

## Choose one browser

1. Inspect the current sessions before opening anything. Prefer the browser
   already shown in Factory's native browser pane.
2. Check that its URL, title and subject match the intended task. A blank
   Chrome DevTools or Grabber tab does not establish access to the user's
   authenticated working browser.
3. If the user's browser already has a supported CDP connection, attach to
   that exact browser/tab using the installed driver's documented controls.
   Do not guess a port or attach to an unrelated session.
4. If it is not attachable, explain the limit. Never silently restart Chrome,
   enable remote debugging, change security settings, copy a locked profile,
   or open the same profile concurrently.
5. Only if necessary and authorized, use one agent-owned browser. Reuse that
   session for the task rather than opening another browser for each command.
   A second browser is a fallback, not the default.

Use the installed driver rather than adding a new streaming service. On
Windows, discover the actual executable with `Get-Command agent-browser`.
Check `--version` and `--help` because bundled skills and the binary may be
out of sync. Do not install or upgrade the browser stack just to obtain a
feature already present.

### Factory-injected connection versus an owned browser

Before choosing a session, inspect the presence (not secret values) of
`AGENT_BROWSER_CDP`, `AGENT_BROWSER_SESSION`, and `FACTORY_DESKTOP_CDP_PORT`.
Factory App can inject its embedded browser's restricted CDP connection and
default session. Overriding only `--session` does **not** create an independent
browser: that new daemon can still attach to the injected endpoint.

Use the injected default session for the native pane. Never print its full
CDP URL, whose path contains an access token. A standalone Chrome DevTools MCP
configured to launch its own browser is a different control path, even if
both initially show `about:blank`.

On Factory App 0.204.0, the native proxy forwards to one replaceable webview
guest. The guest can change while driver metadata still names an old tab.
Check actual DOM URL, nonzero viewport, visible controls and target ownership
before input. Do not fix a hidden pane by blindly forcing CSS visibility or
enter credentials into a zero-size view. A viewport override alone did not
establish durable control in the observed session.

If a truly independent browser is authorized and necessary, remove the
injected CDP/auto-connect/profile/state/restore/provider overrides **only in
that child process environment**, choose one owned session, and use a clean
agent profile. Do not change global environment or copy the user's profile.
Verify an actual owned browser started before claiming isolation. A local
launch in this session timed out and was not proven operational.

## Work in the native live view

Use the Factory browser pane directly when it already shows the session.
Do not generate an HTML file or ask the user to open its source.

Keep the same session name on every command. Typical installed-driver
commands are:

```powershell
agent-browser session list --json
agent-browser --session <existing-session> session info --json
agent-browser --session <existing-session> get url
agent-browser --session <existing-session> snapshot -i
agent-browser --session <existing-session> click @e1
agent-browser --session <existing-session> stream status --json
```

Replace the session and element references with observed values. Re-snapshot
after navigation or a material DOM change. Prefer DOM/accessibility actions;
use live visual inspection for layout, maps, photos and uncertain controls.
Respect the available-tool rules when choosing MCP tools versus a CLI.

The native session stream is separate from saved video recording. Streaming
does not require creating an MP4/WebM or restarting the browser context.
In the tested driver, every session has a loopback WebSocket stream.
`stream status` reports `connected`, `enabled`, `port`, and `screencasting`.
A client must be watching before active screencasting is expected.

If the native pane is unavailable, the bundled **optional** dashboard can
display that same session and its action feed:

```powershell
agent-browser dashboard start
```

Its documented default address is `http://localhost:4848`. Confirm actual
loopback-only binding and port ownership. Do not expose it to the LAN or
Internet, add a reverse proxy, allow arbitrary origins, or print access
tokens. A dashboard in another browser is not automatically the requested
Factory side panel. Disclose this fallback and ask whether it is acceptable.
Do not build an iframe wrapper to paper over a missing native integration.

## Prove the user is watching the right session

- Verify the **current chat's panel is actually open**, not just the guest
  viewport. On Factory 0.204.0, `Show Panel` meant it was collapsed while
  the hidden dashboard still reported a connected stream and changing frames.
  The operator restored it with Show Panel, then the large Browser launcher
  (`Ctrl+Shift+B` in this build). It need not appear as a Browser tab.
  Desktop accessibility calls did not open it reliably; do not claim they did.
  If oversight is lost, pause task input until the operator's view is restored.
- Compare the target URL/title with the viewer's session and current URL.
- Perform one safe, useful action in the real task, such as navigation or
  opening a non-mutating detail view.
- Confirm the resulting page state through the DOM and the live viewer.
- If the operator's view is uncertain, ask once whether they see that exact
  action/page in Factory. Do not infer native-panel success solely from an
  HTTP 200 response, a listening socket, or a successful canvas probe.
- If the user takes over, stop issuing input until they hand control back.
  Never run parallel agents against this same browser.

Announce the next material action briefly. Keep normal browser work moving;
do not demand approval for every click. Pause at the user-requested stage
boundaries, consequential actions, missing authentication, or genuine blockers.

## Panel state is transient — re-attach mechanically, never panic

Factory collapses or blanks the browser pane when the user moves between
sessions or chats. That is routine, not an emergency and not a lost browser.
The actor session, its tabs, and the dashboard survive pane collapse. Do not
restart browsers, re-login, or pause the whole task over it; run the recipe
below (about a minute) and continue.

Proven re-attach recipe (Legion, 2026-10-22):

1. Check the pane session's real DOM (`eval` `location.href`) against its
   tab registry. A registry URL of `http://localhost:4848/` with a DOM of
   `about:blank` or an empty document means the pane webview fell back to
   blank. `reload` may leave it at `about:blank`; `open <dashboard-url>`
   restores it.
2. The bundled dashboard picks the streamed session from the `?port=` query
   parameter (the session's stream port) at page load. Same-page navigation
   adding a query aborts (`net::ERR_ABORTED`, likely an auto-dismissed
   beforeunload); instead click the wanted session's tab row in the
   dashboard's Sessions tab.
3. Radix tabs and session rows need a full synthetic pointer sequence
   (`pointerdown`, `mousedown`, `pointerup`, `mouseup`, `click`) dispatched
   in `eval`; a programmatic `click()` alone does not switch them. React may
   apply the change a second or two later — re-read state before concluding
   failure.
4. Verify the Viewport shows `ws://localhost:4848/api/session/<port>/stream`
   with the owned session's port, and prove frames with a reversible visual
   change on the actor page (e.g. `document.body.style.filter='invert(1)'`,
   compare a canvas pixel fingerprint, then remove it). A static page yields
   identical frames; stillness is not staleness.
5. Input is refused with `Browser pane is hidden; show the browser pane
   before sending keyboard input` while collapsed. The panel is open when
   the edge button reads `Hide Panel`. Accessibility calls did not open a
   collapsed panel reliably in this build; the operator's Show Panel + Browser
   launcher did. Ask once if the recipe cannot restore the view.

After any Factory session/chat switch, re-run the step-1 check before the
next browser action and re-attach silently if needed. Confirm with the user
once per recovery, not per action.

## Avoid screenshot buildup

- Do not save a screenshot after every click or run a screenshot-refresh loop.
- Read DOM state for machine verification; use the live stream for shadowing.
- If a visual decision needs a frame, inspect one through the available
  tool without writing a permanent image when supported.
- Retain only requested or necessary evidence, failure captures and required
  task artifacts. State their paths. Never delete existing files without
  permission.
- Live observation does not replace saved-state readback, verified downloads,
  appraisal photo review, or the report's required maps/images/documents.
- Routine observation should not create HTML viewers, videos, frame archives
  or a second automation stack.

## Authentication and sensitive work

Reuse existing authenticated sessions. Entering a different browser's login
may invalidate a single-session portal, including Titan. Stop and explain
that consequence before any new login. Prefer operator-controlled sign-in
or protected credential tools; never put passwords/tokens into recorded
commands, activity feeds, screenshots, skill files or chat.

An unsigned report is not permission to edit a template, signed report or
cancelled order. Follow the task's own verification and approval rules.
For appraisals, live observation does not authorize certification, signing,
client delivery, duplicate merges or bypassing comp approval.

## Ownership and cleanup

Track which browser, tab, dashboard and process you opened. Leave the user's
existing browser alone. Close only agent-owned resources when the user no
longer needs the live view; do not use a blanket `close --all`. Do not stop a
pre-existing dashboard.

## Tested limits

On Legion, agent-browser 0.37.1 provided a real live canvas stream and command
events from one persistent session. Navigation to Titan reused that session;
the operator confirmed the real sign-in page was visible and interactive.
Bitwarden-backed native login was subsequently authorized. The initial native
credential-hook route failed; the working independent-browser route below
later verified authentication. No report mutation followed this checkpoint.
The normal user Chrome had no CDP debugging connection. The user preferred
native observation and rejected the extra HTML viewer. Do not repeat that
wrapper approach.

The native credential hook in this binary has a fixed 15-second deadline.
Pre-unlocking Bitwarden and setting `BW_SESSION` on the CLI child did not
resolve its timeout; do not assume a running daemon's plugin inherits the
CLI child's environment. Keep secrets out of arguments and files rather than
working around this by exposing them. Stop repeated hook attempts.

Pinned v0.37.1 source confirms credential resolution runs in the daemon.
Later CLI environment changes cannot update that daemon's environment.
Resolution failure returns before the login handler navigates or fills.
The same version also caches invalid top-level session IDs and ignores a
replacement session ID when updating an already tracked target. A responsive
CDP error is not proof the page attachment is healthy.

After that timeout, cached tab listing still showed Titan, while DOM access
and reselecting the same tab failed with `No target with given session id`.
A cached URL or stream alone does not prove current control or authentication.
Preserve the browser, report the lost-control boundary, and agree on a bounded
recovery or operator takeover before further login actions.

## Working recovery on Legion, 2026-10-22

The proven recovery used the existing installed agent-browser and bundled
Chrome, not another streaming framework:

1. Remove Factory's injected CDP/auto-connect/profile/state/restore/provider
   overrides in the launch child's environment only. Choose one owned session.
2. Use the installed automation Chrome executable and a managed background
   launch (`Execute` with `fireAndForget: true`) so its lifetime is explicit.
   The successful run used
   `C:\Users\lkmot\.agent-browser\browsers\chrome-154.0.8037.57\chrome.exe`.
   This is an observed installed path, not a portable version pin.
3. Verify actual DOM access, visible controls, and a loopback CDP transport
   distinct from Factory's native proxy. A launch acknowledgement is not proof.
4. For **every owned-browser command**, remove `AGENT_BROWSER_CDP` again in
   that command's child environment and specify the owned session. Execute
   calls do not share environment changes.
5. For **viewer commands**, retain Factory's injected connection/default
   session. Open the existing bundled loopback dashboard in that native pane,
   select the owned browser's tab, then select Viewport. Do not mistake old
   cached sessions for the current actor.
6. Verify `screencasting: true`, actual viewer frames, and a useful action
   with DOM readback. This run confirmed two distinct in-memory canvas frames
   across four samples and a focused Titan username field. Save no frame files.

On the dashboard's Radix tabs, a programmatic `click()` alone did not select
the tab; its normal left `mousedown` event did. Coordinate clicks in a
zero-size native pane did not reliably hit controls. Restore usable viewer
layout, inspect state, and verify the exact selected session.

The independent browser exposed normal CDP, so existing installed Playwright
could connect to that same browser. Existing `agent.portal_auth` and the
scoped provider resolved the approved Bitwarden item in process memory.
Credentials passed directly to Playwright locators, never command arguments,
activity-feed parameters or credential files. No new credential plugin or
secret-bearing file was needed. Do not close the attached browser on exit.

One submit redirected through `titanoffice.alamode.com/Orders/Index`.
Immediate page evaluation encountered a navigation-context change; a
subsequent read-only check verified Log Out and no challenge. Navigating the
same browser to `https://titanappraisal.com/Desktop` then verified the actual
report Drive, file grid, visible New action and no visible password field.
An intermediate non-Desktop redirect is not automatically a failed login.
Never resubmit merely because a verification crossed navigation.

References:

- https://agent-browser.dev/streaming
- https://agent-browser.dev/dashboard
- https://docs.factory.com/software-factory/droid-control.md
