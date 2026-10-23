# Tool Input Catalog — High-Signal Finds

Source: full GetInputList dump 2026-01, phase 0 of capability plan. Full ID lists in `catalog.json`.

## Transform
- `XSize` / `YSize` — independent per-axis scaling (squash/stretch, letterbox fills).
- `Pivot` — rotate/scale around arbitrary point (corner-anchored wipes).
- `Edges` — **Wrap mode eliminates black edges during Ken Burns moves.** Not yet probed with this exact value name.
- `MotionBlur` + `ShutterAngle` — free motion blur on transforms.
- `FlipHoriz` / `FlipVert` / `InvertTransform` / `CorrectEdges`.

## Merge
- **Merge has its own Center / Size / Angle / Flip / Edges** — a Transform tool upstream of a Merge is often unnecessary. Set fg position/scale directly on the Merge.
- `ApplyMode` — blend modes (screen/add = glow, multiply = shadow). Value strings unprobed.
- `Operator` — under/over/in/held-out operators.
- `PerformDepthMerge` — z-compositing when merging 3D.
- `ProcessWhenBlendIs00` — performance: turn off to skip rendering invisible fg.
- `BurnIn`, `Gain`, `Channels`, `SubtractiveAdditive`.

## Background
- `Gradient` + `GradientType` + `GradientInterpolationMethod` — native gradients, no need for Background+Mask sandwich.
- `Start` / `End` / `Offset` — animate gradient position.
- Per-corner RGBA (`TopLeftRed`...`BottomRightAlpha`) for 4-corner gradients.

## TextPlus (309 total inputs — highlights)
- **3D rotation at three nesting levels**: `AngleX/Y/Z` (whole text), `LineAngleX/Y/Z`, `WordAngleX/Y/Z`, `CharacterAngleX/Y/Z` — 3D title fly-ins with zero Text3D.
- `Perspective` — enables the 3D rotation rendering.
- `Opacity1` — per-shading-element opacity; **better than Merge.Blend for text fades** (fades the glyph, not the whole layer).
- `Enabled1..8` — toggle shading elements (e.g. kill outline element).
- `Scroll` + `ScrollPosition` — scrolling credits built in.
- `Style` — font weight; `Font` — family; `CharacterSpacing`, `LineSpacing`.
- `LayoutType` / `LayoutWidth` / `Wrap` — paragraph boxes; `HorizontalJustificationLeft` etc.
- `ShadingGradient1` — gradient-filled text.
- `FitCharacters`, `Clip` (overflow clipping).
- `MotionBlur`.

## MediaIn
- `Loop`, `HoldFirstFrame` / `HoldLastFrame` — extend short clips without retimes.
- `Reverse` — reverse playback.
- `AudioTrack` / `SoundOffset` — audio routing inside Fusion comp.
- `ClipTimeStart` / `ClipTimeEnd` — readback of source trim.

## Bridge readback traps (learned during this dump)
- `comp.CurrentTime = N` does NOT move the evaluation playhead; indexed/value readbacks at "changed" time silently return playhead-time values. Verify animation via `GetKeyFrames()` (returns {index: frame}) + render, not by sampling.
- `Input.GetValue()` and `Input.GetValuesDict()` are NOT exposed by this bridge (NoneType). Use `GetKeyFrames()`, indexed `input[k]` (dict for Points: keys "1"=x-ish,"2"=y-ish), or render-based proof.
- Deleting tools by auto-assigned name is dangerous: name availability depends on existing tool names. Dump scripts must tag their own tools (e.g. SetAttrs TOOLS_Name prefix `ZZ_DUMP_`) and delete only those.
