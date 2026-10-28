# Deliver / Render — deliver-render.md

Class: `Project` render methods + `RenderSettings`/`RenderJobInfo`/`RenderJobStatus` TypedDicts (in stub).

## The verified pipeline ✅

```
proj.SetCurrentRenderFormatAndCodec("MP4", "H264")     # format/codec live HERE, not in RenderSettings
proj.SetRenderSettings({"TargetDir": dir, "CustomName": name, "ExportVideo": True,
                        "ExportAudio": False, "SelectAllFrames": True,
                        "ReplaceExistingFilesInPlace": True})
job = proj.AddRenderJob()                               # returns id string
proj.StartRendering([job])                              # TAKES A LIST
proj.GetRenderJobStatus(job)                            # poll until JobStatus in Complete/Failed/Cancel
```

⚠️ Traps (all verified):
- Settings key is `TargetDir` — NOT `TargetDirClr`. Wrong keys silently no-op and the queue
  inherits a stale path → "render path inaccessible" UI errors.
- `TargetDir` must exist BEFORE `AddRenderJob`. (Sandbox blocks os — `run_script_unsafe` mkdir.)
- `SetRenderSettings` can return False even when settings applied — trust
  `AddRenderJob` non-empty id + `len(GetRenderJobList())` increasing, not the bool.
- No format/codec keys exist in `RenderSettings`; wrong-format settings corrupt the whole queue state.
- PNG stills: `SetCurrentRenderFormatAndCodec("png","")` may not stick — MP4 renders anyway.
  Prefer `proj.ExportCurrentFrameAsStill(filePath)` 🔌 for stills (untested, cleaner path).

## Settings reference

Full `RenderSettings` TypedDict in the stub: MarkIn/MarkOut, UseUniqueFilenames,
VideoQuality ('Least'..'Best' or bitrate int), PixelAspectRatio, EncodingProfile ('Main10'),
MultiPassEncode (H.264), NetworkOptimization, ExportAlpha/AlphaMode, ExportSubtitle,
DataBurnIn, TimelineStartTimecode, ClipStartFrame.

Status: `RenderJobStatus` includes JobStatus, Completion, OutputFilename.

## Presets & QuickExport

- 🔌 `GetRenderPresetList`, `LoadRenderPreset`, `SaveAsNewRenderPreset`, `UpdateRenderPreset`,
  `SetQuickExportEnabledForRenderPreset`, `RenderWithQuickExport(preset, QuickExportRenderSettings)`
  (fire-and-forget style export — promising for batch, untested).
- 🔌 `GetRenderFormats()` / `GetRenderCodecs(ext)` — enumerate valid format/codec pairs
  instead of guessing strings.

## Batch pattern (production shape)

1. mkdir per-variant dirs (run_script_unsafe).
2. For each variant: SetCurrentRenderFormatAndCodec → SetRenderSettings → AddRenderJob
   (queue N jobs before starting — queue is cheap).
3. One `StartRendering()` over all job ids, then poll `IsRenderingInProgress()` +
   per-job status until all terminal. Verify every OutputFilename on disk before "done".
