# Edit / Timeline — edit-timeline.md

Classes: `Timeline`, `TimelineItem` (signatures in `.methods.txt`).

## Timeline management

- ✅ Find a timeline by name: loop `proj.GetTimelineByIndex(i)` comparing `GetName()` —
  ⚠️ no reliable `GetTimelineByName` on this build.
- ✅ `proj.SetCurrentTimeline(tl)` before anything that acts on "current".
- 🔌 `DuplicateTimeline`, `Export(fileName, exportType, exportSubtype)` (EDL/FCPXML/DRT/OTIO —
  types in stub), `ImportIntoTimeline`, `SetStartTimecode`, `SetSettings(TimelineSettings)`.

## Inserting generators / titles

- ✅ `tl.InsertFusionTitleIntoTimeline("Text+")` — inserts on track 1 at playhead (creates its
  own comp on the item). It does NOT stack over existing clips; it lands beside them.
- 🔌 `InsertGeneratorIntoTimeline`, `InsertFusionCompositionIntoTimeline`, `InsertOFXGeneratorIntoTimeline`.
- ⚠️ For a title OVER footage, prefer building a comp on the footage item (Fusion page model)
  instead of inserting a title clip and trying to move it to another track.

## Clips on tracks

- ✅ `tl.GetItemListInTrack("video", 1)` — trackType is lowercase string "video"/"audio".
- ✅ Delete: `tl.DeleteClips(items, False)` (rippleDelete second arg). There is NO
  `TimelineItem.Delete()`.
- ✅ Playhead: `tl.SetCurrentTimecode("01:00:00:00")`.
- 🔌 Track ops: `AddTrack`, `DeleteTrack`, `SetTrackEnable`, `SetTrackLock`, `SetTrackName`,
  subtypes (e.g. stereo) via `GetTrackSubType`.

## Markers

- 🔌 `AddMarker(frameId, color, name, note, duration, customData)` — customData is queryable
  via `GetMarkerByCustomData` (use for machine-driven selects: store cut IDs in customData).
- 🔌 `GetMarkers()` → dict[frame] → MarkerInfo.

## Auto-editing (Studio)

- ✅ `DetectSceneCuts()` — verified 21.1, returns True, cuts created. (Testsrc footage; real
  footage cut accuracy untested — treat detection quality as unverified, API as verified.)
- ✅ `CreateSubtitlesFromAudio()` — verified 21.1: produced 7 accurately-timed subtitle
  items from a spoken WAV (correct transcription, ~60-frame segments). Works with defaults
  ({}); captions land on a subtitle track readable via `GetItemListInTrack("subtitle", 1)`.
- 🔌 `AutoAlignClips(items, AutoAlignOptions)`, `SmartSwitch` settings
  (multicam, see stub `SmartSwitchSettings`), `CreateCompoundClip`, `CreateFusionClip`.

## Voice isolation (per audio track)

- 🔌 `GetVoiceIsolationState(trackIndex)` / `SetVoiceIsolationState(trackIndex, state)`.

## TimelineItem essentials (from methods file)

- ✅ `item.AddFusionComp()` / `GetFusionCompByIndex(1)` / `GetFusionCompCount()`.
- ✅ `item.GetName()`, `GetStart()/GetEnd()` (⚠️ None on an empty timeline).
- 🔌 Properties via `GetProperties()/SetProperties()` (see `TimelineItemProperties` TypedDict:
  transform, crop, retiming, speed — `SpeedOptions`), `GetFusionCompNameList`,
  versions, takes (`TakeInfo`).
