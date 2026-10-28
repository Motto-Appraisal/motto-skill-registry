# Promotional Video Build Patterns (proven end-to-end 2026-09-14)

Deliverable proof: `motto_promo_v6.mp4` — 26.8s 1080p30 promo, 4 scenes, SAPI VO +
music bed, verified by vision checks + 9/9 unique frame MD5s. Build script: this
session's `run_script_unsafe` calls (patterns below are the distilled, reusable form).

## CRITICAL project setup (order matters)
```python
proj = pm.CreateProject("Name")
proj.SetSetting("timelineFrameRate", "30")   # and resolution
proj.SetSetting("colorScienceMode", "davinciYRGB")   # MANDATORY — see trap 1
```

## The 6 traps that cost this session (ALL verified empirically)
1. **Color management**: API-created projects default to `davinciYRGBColorManagedv2`.
   It silently transforms every Fusion tool color (navy→gray-blue, gold→clipped yellow,
   white text → invisible on brightened bg). Set `davinciYRGB` IMMEDIATELY.
2. **TextPlus color**: set `Red1/Green1/Blue1` (shading element 1). Setting
   `Red/Green/Blue` instead CORRUPTS the tool into a full-frame solid rectangle of
   the fill color. Symptom: solid white/gold frames with no glyphs.
3. **Auto MediaIn1 is unbound**: comps from `item.AddFusionComp()` contain a
   MediaIn1 with NO source binding (no MEDIA attrs) → renders WHITE. For generated
   graphics, use an explicit `Background` tool as the base layer instead.
4. **Masks don't connect**: `tool.EffectMask.ConnectTo(rect.Output)` returns False
   and silently does nothing. Avoid RectangleMask-based designs via the bridge;
   use text rules (underscores) or full-frame layers instead.
5. **MediaOut auto-naming**: `AddTool("MediaOut")` creates MediaOut2 if MediaOut1
   exists; the item only renders MediaOut1. Always `FindTool("MediaOut1")` first.
6. **Still exports are unreliable**: `ExportCurrentFrameAsStill` may return True but
   write nothing, and `SetCurrentTimecode` is async (readback can lag). Renders +
   ffmpeg frame extraction are the only ground truth.

## Proven promo assembly pattern
1. Assets: SAPI narration per scene (`System.Speech`) → ffprobe durations →
   scene_frames = (dur_seconds + pad) * fps. Music bed via ffmpeg sines + tremolo +
   lowpass + fades, volume ~0.35.
2. Timeline: `base` video clip appended N times with `{"mediaPoolItem", "startFrame",
   "endFrame", "mediaType": 1, "trackIndex": 1}` — endFrame controls scene duration
   exactly. VO: same with `mediaType: 2, trackIndex: 1, recordFrame: scene_start`.
   Music: `mediaType: 2, trackIndex: 2` — **AddTrack("audio") first if track 2 absent**.
3. Per-scene comps on each video item: chain of Merges
   (Background base → text layers), each text layer fade-in via
   `merge.Blend.SetExpression("min(1, max(0, (time - START) / DUR))")` — comp-local
   `time` in expressions is reliable (splines also work, expressions preferred).
4. Motion: Transform Center expression (rise/settle) + Size BezierSpline keys
   (overshoot: {0:0.5, 15:1.12, 28:1.0}).
5. Fade-to-black at promo end: final Merge with full-frame black Background as fg,
   Blend expression `min(1, max(0, (time - 140) / 22))` (RISING black, not falling).
6. Verify: render → `ffmpeg -ss t -i out.mp4 -frames:v 1` frames → per-frame MD5
   (all unique = motion proof) → Qwen vision check per scene → ffprobe audio stream.

## Verification toolkit built this session
- `bandscan.py` / `pixscan.py` pattern: ffmpeg crop+signalstats YAVG per region and
  raw RGB pixel reads — diagnose layout/color without vision API cost.
- `describe_frame.py`: one-off Qwen detailed frame description (richer than
  vision_check.py's fixed schema) — uses Doppler QWEN_CLOUD_API_KEY.
