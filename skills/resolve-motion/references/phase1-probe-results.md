# Phase 1 Media Plumbing Probe Results — 21.1, ResolveMCP bridge

Test assets: synthetic multicam in `~/Videos/motto-test-footage\` (camA/camB mp4s
with embedded audio + separate recorder WAV; transient beep pattern for waveform sync test;
SAPI voice WAV for captions). Probe project: `Motto Probe Phase1`.

## Verified working (✅)
| API | Evidence |
|---|---|
| `mp.ImportMedia([paths])` | 4 clips in, all returned as MediaPoolItems |
| `mp.AddSubFolder(root, name)` | Cams/Audio bins created |
| `mp.MoveClips([items], folder)` | audio clip moved (true); video move returned false once — flaky, retry |
| `mp.CreateTimelineFromClips` | 2 video + 3 audio clips, correct structure |
| `tl.DetectSceneCuts()` | True, cuts created |
| `tl.CreateSubtitlesFromAudio()` | 7 accurate timed captions from spoken WAV; subtitle items via `GetItemListInTrack("subtitle", 1)`; item name = caption text |
| `proj.GenerateSpeech` surface | callable, returns str error (see below) |

## Blocked / broken (❌ with workarounds)
1. **`mp.AutoSyncAudio` → always False.** Tried: waveform mode (const == 0, confirmed correct),
   pure-tone audio, transient-rich audio, fresh items outside any timeline, pre-selected clips.
   No error surfaced. **Workaround (adopted):** ffmpeg-extract WAVs → numpy cross-correlation →
   place with explicit recordFrame offsets. Deterministic, no Resolve dependency.
2. **`GenerateSpeech` → "Required Package, 'AI Speech Generator' is not Installed."**
   Fix path: install AI Speech Generator component. **Interim:** Windows SAPI
   (`System.Speech`) TTS → WAV → imports fine and transcribes cleanly via captions API.

## New traps recorded
- `resolve.AUDIO_SYNC_WAVEFORM == 0` (same value as presumed TIMECODE default — verify constants
  numerically, don't trust names).
- Bridge exposes a **subset** of the stub; `dir()` the object before calling. Surface dump:
  `bridge-surface.json`. GenerateSpeech lives on **Project** there, not where the stub says.
- `comp.CurrentTime = N` does not move the evaluation playhead; don't sample animated values
  that way — use `GetKeyFrames()` + render-based proof.
- Sandbox forbids `open()`/file IO inside run_script — keep comp scripts pure, persist data
  by returning it and writing from outside.
- Dump scripts that AddTool must tag their tools (e.g. `ZZ_DUMP_` prefix) — delete-by-name can
  destroy real comp nodes (this cost us a Merge2/Transform1 rebuild).
