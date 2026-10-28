# resolve-motion

Drive DaVinci Resolve Studio 21.1+ via the native MCP server (`davinci-resolve__*` tools) for
motion graphics, automated assembly, and renders. Load this skill before any Resolve automation
session.

## When to use

- Any task touching Resolve: timelines, media pool, Fusion comps, render queue, AI transcription.
- Motion graphics / title cards / lower thirds built or driven by script.

## Companion skills (installed 2026-09-14, evaluation period)

Twelve external skills are installed alongside this one (junctioned from
`~/.factory/knowledge/external-skills/` — `git pull` there to update):

- **ChaiWithJai/davinci-resolve-claude-skills** — craft layer: titles-and-lower-thirds,
  export-multi-platform, audio-cleanup-podcast, color-grade-webcam, cut-screen-recording,
  social-editor, project-template, troubleshooting. Grounded in the six official Blackmagic
  Resolve 20 training PDFs (wiki summaries + page citations). Use for production *judgment*.
  Note: their scripts attach to Resolve's external scripting API and assume `External scripting
  using: Local`; only macOS default path found is the render output dir (override it).
- **TerminalSkills/skills → davinci-resolve-api-reference** — API reference breadth. Use for
  lookups; does NOT contain the 21.1 gotchas in this file.

Division of labor: this skill = automation mechanics + native MCP bridge. Companions = craft
and post-production workflow knowledge. Load both for real video projects.

## Department references (read before working on that page)

`references/` contains per-department API docs distilled from the shipped stub (copies of
`DaVinciResolveScript.pyi` + `fusion_api.pyi` live there — the authoritative source):

- `references/README.md` — index + verification legend (✅ verified / 🔌 available / ⚠️ trap)
- `references/media-pool.md` — import, bins, stills, timeline-from-clips
- `references/edit-timeline.md` — timelines, tracks, clips, markers, auto-edit
- `references/fusion-comp.md` — comps, keyframes, expressions, wiring, Text+ styling
- `references/deliver-render.md` — render queue, presets, QuickExport, batch pattern
- `references/color-fairlight-ai.md` — Color/Gallery, Fairlight/audio, Studio AI tools

Rule: full signatures live in `references/<Class>.methods.txt` — grep those, never guess
method names. Anything marked 🔌 is stub-verified but not yet exercised live; test once on a
sandbox timeline before batch use. Anything ⚠️ is a known trap documented from a live failure.

## Setup facts

- Tools load as `davinci-resolve__*` in new sessions (stdio via `ResolveMCP (macOS: see Platform notes)`, defined in `~/.factory/mcp.json`).
- Resolve must be running. `launch_resolve` starts it. Headless: `"/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/MacOS/Resolve" -nogui` (Studio only),
  then `get_resolve_status` until `running: true`. Full scripting API works with no UI.
- Helper library: `~/.factory/knowledge/resolve-kit/resolve_kit.py` (functions are pasted into
  `run_script` calls, not imported) and `templates.py` (parameterized builders).

## Hard-won API rules (all verified against 21.1.0.17 — do not rediscover)

1. `SetInput(id, value, time)` silently no-ops unless the input has a spline modifier.
   Sequence: `tool.AddModifier(input, "BezierSpline")` THEN `SetInput(input, value, frame)`.
2. Keyframes are 0-based within the clip's Fusion comp. Modifier splines show up as tools
   (e.g. `Transform1Size`) — addressable via `comp.FindTool("Transform1Size")`.
3. Fusion points: pass Python LISTS `[x, y]`, never set-literals `{x, y}` (unordered → silent fail).
4. Point-input animation (Center) is NOT keyframeable through the bridge. Animate with a
   Transform tool (Size/Angle scalars) instead of sliding Center.
5. Render: `SetCurrentRenderFormatAndCodec("MP4", "H264")` — format/codec are NOT RenderSettings keys.
   `SetRenderSettings({"TargetDir": ...})` — the key is `TargetDir`, not `TargetDirClr`.
   Target dir MUST exist first (sandbox blocks `os`; use `run_script_unsafe` for mkdir).
   `StartRendering([job_id])` takes a list. Poll `GetRenderJobStatus(job_id)` in separate calls.
6. Placement: `CreateEmptyTimeline` and `AppendToTimeline` are on MediaPool. `GetTimelineByName`
   is unreliable — loop `GetTimelineByIndex`. Deleting timeline items: `Timeline.DeleteClips`.
7. `run_script` times out at ~10s and blocks `os`/`sys` imports. One builder or one poll per call.
   `run_script_unsafe` allows filesystem but requires Resolve running.
8. Text color = TextPlus shading level 1: inputs `Red1`/`Green1`/`Blue1` (0-1 floats).
9. TextPlus gradient: `Type1=1` + `ShadingMappingAngle1=-90` + `ShadingMappingLevel1=1` (verified
   by render). Alignment = `HorizontalJustificationLeft/Center/Right` action inputs (no "Anchor"
   inputs exist). Setters on shading inputs return None but DO apply — verify by readback.
10. COORDINATE CONVENTION: the Inspector's Layout Y (negative = below center) is INVERTED vs the
    scripting bridge: lower-third in comp space = Center `[x, 0.25-0.32]` (Y up, 0..1).
    Confirmed by render + vision check.
11. ALWAYS verify a Fusion comp's `MediaOut1` has an input connected — an unconnected MediaOut
    renders BLACK with no error (failure signature: vision/eyeball check shows "no visible text").
12. Agent self-verification loop: render still → `vision_check.py <frame>` (Qwen vision via
    Doppler QWEN_CLOUD_API_KEY) → structured JSON pass/fail. Use after ANY layout-sensitive build.
13. PNG stills: `SetCurrentRenderFormatAndCodec("png", "")` may NOT stick — MP4 renders anyway.
    If a still is needed, render MP4 and extract the frame with ffmpeg.
14. COLOR MANAGEMENT: API-created projects default to `davinciYRGBColorManagedv2`, which
    silently transforms every Fusion tool color (navy→gray-blue, gold→clipped yellow,
    white text invisible). FIRST call on a new project:
    `proj.SetSetting("colorScienceMode", "davinciYRGB")`.
15. Setting `Red/Green/Blue` (non-element) on TextPlus CORRUPTS the tool: it renders as a
    full-frame solid rectangle of the fill color (no glyphs). Failure signature: uniform
    white/gold frames. Only `Red1/Green1/Blue1` is safe (rule 8 exists for a reason).
16. Auto-created `MediaIn1` inside `item.AddFusionComp()` comps has NO source binding and
    renders WHITE (no MEDIA attrs at all). For generated graphics use an explicit
    `Background` tool as the base layer; don't trust auto MediaIn on video items.
17. Masks are unusable via the bridge: `tool.EffectMask.ConnectTo(rect.Output)` returns
    False silently. Design without RectangleMask (use text rules / full-frame layers).
18. `AddTool("MediaOut")` creates MediaOut2 when MediaOut1 exists — the item renders only
    MediaOut1 (extra outputs are ignored → passthrough confusion). Always FindTool first.
    Same discipline for MediaIn. NEVER delete modifier tools via FindTool+Delete
    (corrupts the parent tool's rendering).
19. `SetCurrentTimecode` is ASYNC — readback may lag (sampled frames were wrong). And
    `ExportCurrentFrameAsStill` can return True while writing NOTHING. Renders + ffmpeg
    frame extraction are the ONLY ground truth for verification.
20. `AppendToTimeline` audio to track 2 requires `tl.AddTrack("audio")` first (silent null
    items otherwise). Promo assembly pattern + verification toolkit:
    `references/promo-build-patterns.md`.

## Standard workflows

### Intro/title card (parameterized)
1. `run_script_unsafe`: `os.makedirs(out_dir)`.
2. Generate/import background (AI image via GenerateImage → `ImportMedia` → `AppendToTimeline`).
3. Paste `templates.py:INTRO_HEAD` with `PARAMS` filled (runs inside the clip's Fusion comp).
4. `kit_render_current_timeline` → poll `kit_render_status` → verify file with `run_script_unsafe`.

### Session context probe
First call of any Resolve session: paste `kit_current_state()` — project, timelines, render state.

### Verified render round-trip
Queue job → poll every call until `Complete` → verify file exists and size > 0 via
`run_script_unsafe` before claiming success.

## Gotchas / failure signatures

- `TypeError: 'NoneType' object is not callable` → wrong owner class (check items 6) or attribute
  is absent on this build — search the stub (`search_scripting_api`) instead of guessing.
- Render job never appears in queue → TargetDir missing/invalid, or settings silently rejected
  (check `SetRenderSettings` returned True).
- "Render path inaccessible" UI errors → stale invalid TargetDir from a previous bad call.
