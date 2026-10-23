# Color / Gallery — color-gallery.md (mostly 🔌 untested)

Classes: `ColorGroup`, `Gallery`, `GalleryStill`, `GalleryStillAlbum`; CDL TypedDict in stub.

- 🔌 `proj.AddColorGroup(name)` / `GetColorGroupsList()` / `DeleteColorGroup` — clip groupings
  for grade management. ColorGroup methods (pre-clip/post-clip) in methods file.
- 🔌 CDL workflow: `CDL` TypedDict (slope/offset/power/sat) — applied via TimelineItem
  color methods (see TimelineItem.methods.txt: `SetCDL`, LUT methods, `GetNodeGraph` →
  `Graph` class exposes the color node graph — same Graph object as Fusion node graphs).
- 🔌 Stills: `tl.GrabStill()` / `GrabAllStills(source)` → `Gallery` albums
  (`GetGallery()` on Project) — grade references, before/after proof frames.
- 🔌 `proj.LoadBurnInPreset(name)` — data burn-in for dailies/QC renders.
- ⚠️ Color page per-clip grade APIs live on TimelineItem in the stub — verify names there,
  not from memory (the color API was reworked across 18/19/20/21).

# Fairlight / Audio — fairlight-audio.md (mostly 🔌 untested)

- 🔌 `tl.NormalizeAudioLevel(items, NormalizeAudioOptions)` — loudness normalize with target
  modes from `GetNormalizeAudioModes()` (platform targets: YouTube/broadcast).
- ❌ `mp.AutoSyncAudio(items, AudioSyncSettings)` — **broken in practice on 21.1 bridge**:
  returns False in every variant tried (waveform mode 0 with pure-tone audio, transient-rich
  audio, fresh items outside timelines, with clips selected via SetSelectedClip). No error
  string. WORKAROUND (adopted): compute offsets ourselves — extract WAVs with ffmpeg,
  cross-correlate in Python, then place clips with recordFrame offsets. More deterministic
  anyway.
- 🔌 `tl.SetVoiceIsolationState(trackIndex, VoiceIsolationState)` — Studio AI voice isolation.
- ❌ `proj.GenerateSpeech(SpeechSettings)` — exposed on **Project** (not Resolve/Timeline;
  bridge dir() confirmed) but returns the string "Required Package, 'AI Speech Generator' is
  not Installed." Fix: reinstall/enable AI Speech Generator component (installer option or
  separate AI models download). Fallback proven: Windows SAPI TTS (`System.Speech`) writes
  WAVs that Resolve imports and transcribes cleanly.
- 🔌 `proj.ApplyFairlightPresetToCurrentTimeline(presetName)`.
- 🔌 `proj.InsertAudioToCurrentTrackAtPlayhead(path, startOffsetSamples, durationSamples)`.
- 🔌 `mp.CreateStereoClip(left, right)`; audio track subtypes via `tl.AddTrack("audio", subType)`.

# Studio AI Tools — ai-tools.md (mostly 🔌 untested; Studio only, 16GB+ VRAM recommended)

TypedDicts in stub: `Transcription`, `TranscriptionSegment`, `TranscriptionWord`,
`AutoCaptionSettings`, `DeblurOptions`, `SpeechSettings`, `DolbyVisionAnalysisType`.

- ✅ `tl.CreateSubtitlesFromAudio(AutoCaptionSettings)` — verified 21.1: 7 timed, correctly
  transcribed subtitle items from spoken WAV; accessible via `GetItemListInTrack("subtitle", 1)`
  (each item's name = caption text, GetStart/GetEnd = frames).
- 🔌 Transcription access via MediaPoolItem (see methods file: transcription getters —
  word-level timing drives caption-only finishing passes).
- 🔌 AI motion deblur: TimelineItem methods with `DeblurOptions` → new clips.
- 🔌 `proj.ResetIntellisearchAnalysis()` + Intellisearch analysis calls (face ID search) —
  Media page analysis; `AnalyzeDolbyVision(items, analysisType)` for HDR trims.
- ⚠️ GPU gate: our Legion RTX 3070 Ti Laptop has 8GB VRAM vs BMD's 16GB recommendation for
  AI tools on Windows — expect slow runs or refusals; test on short clips before promising.

# Project / app management — project-manager.md

- ✅ `pm.CreateProject(name)` returns None if the name exists — then `LoadProject(name)`.
- 🔌 Databases: `pm.GetDatabaseList()`, `CreateProjectDB` etc. (see methods file);
  `ExportProject`/`ImportProject` for archive/backup flows.
- 🔌 `resolve.OpenPage("deliver")` etc. — pages: media, cut, edit, fusion, color, fairlight,
  deliver. OpenPage can block >10s; isolate in its own run_script call with a longer timeout.
- 🔌 Headless: `Resolve.exe -nogui` (Studio only) — full scripting API, no UI. Verified ✅.
