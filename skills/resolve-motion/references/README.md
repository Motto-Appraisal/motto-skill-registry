# resolve-motion — Department References

Per-department API reference for DaVinci Resolve Studio 21.1 scripting, distilled from the
shipped stub (`DaVinciResolveScript.pyi` in this folder — the authoritative source; 2,765 lines)
plus live-session verification. Fusion-side API is in `fusion_api.pyi`.

## Legend

- ✅ **VERIFIED** — executed against live Resolve 21.1.0.17 and result confirmed (often via render + vision check)
- 🔌 **AVAILABLE** — exists in the stub for 21.1, not yet exercised here; trust the stub, test before batch use
- ⚠️ **TRAP** — verified failure mode; read before using

## Departments

| File | Page(s) | Core classes |
|---|---|---|
| `media-pool.md` | Media | MediaPool, MediaPoolItem, MediaStorage, Folder |
| `edit-timeline.md` | Edit / Cut | Timeline, TimelineItem, markers, multicam |
| `fusion-comp.md` | Fusion | FusionComp, keyframes, expressions, transforms |
| `color-gallery.md` | Color | ColorGroup, CDL, Gallery, stills |
| `fairlight-audio.md` | Fairlight | NormalizeAudioLevel, VoiceIsolation, AutoSync, GenerateSpeech |
| `deliver-render.md` | Deliver | RenderSettings, render queue, QuickExport, stills |
| `ai-tools.md` | Studio AI | Transcription, AutoCaption, Deblur, Dolby Vision analysis |

## Method signatures

Every class's full signature list lives beside these docs as `<ClassName>.methods.txt`
(extracted from the stub). When a doc says "see methods file", grep it — do not guess names.

## Standing rules (details in SKILL.md)

1. Any call returning `None`/`False` where you expected a value: treat as unverified, read back
   or probe the stub. Silent no-ops are the #1 failure mode of this API.
2. Animation: spline modifier must exist before time-based SetInput (scalars) — or use
   SetExpression (verified for Point inputs).
3. After building any comp: assert MediaOut1 input connectivity before rendering.
