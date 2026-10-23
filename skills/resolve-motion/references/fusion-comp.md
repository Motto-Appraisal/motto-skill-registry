# Fusion Comp — fusion-comp.md

Classes: `FusionComp` (Resolve bridge) + full Fusion tool API (`fusion_api.pyi` in this folder).

## The verified motion toolbox (all ✅ against 21.1.0.17)

### Scalar keyframes
```
tool.AddModifier("Size", "BezierSpline")      # modifier FIRST
tool.SetInput("Size", 0.6, 0)                 # then time-based keys
tool.SetInput("Size", 1.0, 20)
tr.Size[13]                                   # readback MUST use attribute indexing
```
⚠️ `GetInput("Size")` returns a plain scalar — per-frame reads need `tool.Size[frame]`.
⚠️ Modifier splines appear in `comp.GetToolList()` as `<Tool><Input>` (e.g. `Transform1Size`)
and are themselves addressable: `comp.FindTool("Transform1Size")`.

### Position animation via expressions (Point inputs are NOT spline-keyable)
```
t1.Center.SetExpression("Point(-0.1 + 0.2*(0.5 - 0.5*math.cos(math.pi*math.min(time/20,1))), 0.3)")
t1.Center.GetExpression()   # verify it took
t1.Center[30]               # evaluate at frame (returns dict {1:x, 2:y, 3:z})
```
⚠️ A failed expression silently falls back to the static default — ALWAYS readback a mid-clip
frame and assert it differs from the default (e.g. Ken Burns `1.0 + 0.12*time/150` read back 1.0).
Coordinate space: normalized 0..1, Y up; `time` is 0-based comp frame.

### Wiring
```
m1.Background.ConnectTo(mi.Output)      # bg under
m1.Foreground.ConnectTo(tr1.Output)     # fg over
mo.Input.ConnectTo(m2.Output)           # final MUST reach MediaOut1
```
⚠️ Unconnected `MediaOut1` renders BLACK with no error. Assert connectivity before render:
`bool(mo.Input.GetConnectedOutput())`.

### Text styling (TextPlus)
- Color: `Red1/Green1/Blue1` (shading element 1). Font: `SetInput("Font", "Open Sans")`.
- Alignment: `HorizontalJustificationLeft` (action input, set to 1) — there are NO "HAnchor" inputs.
- Gradient: `Type1=1` + `ShadingMappingAngle1=-90` + `ShadingMappingLevel1=1` — ⚠️ verify
  visually; a bad gradient recipe can render text invisible (vision-check the output).
- 309 inputs total — enumerate with `t1.GetInputList()` → `INPS_ID` attrs, never guess names.
- ⚠️ Note: `HorizontalJustificationLeft`, `ShadingMappingAngle1` etc. are **runtime tool
  inputs** (via GetInputList, verified by render) — they do NOT appear in any .pyi stub.
  Stub-absence is not evidence a tool input is wrong; the reverse also holds: never invent
  tool inputs, enumerate them.

## Coordinate conventions

- Comp frames are 0-based over the clip duration; timeline start timecode is irrelevant here.
- ⚠️ Inspector Layout Y (negative = below center, UI) is INVERTED vs bridge values:
  lower-third title in the bridge = `Center [0.1..0.15, 0.25..0.32]`.

## 3D (Blenderish territory) — 🔌 not yet exercised

Stub hints: ImagePlane3D, Text3D, Merge3D, cameras/lights via `comp.AddTool(...)`,
Krokodove tools (21.x), `Fusion` class in fusion_api.pyi. Probe pattern: same as above —
AddTool, wire, assert MediaOut, render 1 frame, vision-check — before committing to a scene.
