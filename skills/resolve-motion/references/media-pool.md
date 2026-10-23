# Media Pool — media-pool.md

Classes: `MediaPool`, `MediaPoolItem`, `MediaStorage`, `Folder` (signatures in `.methods.txt`).

⚠️ Placement trap: `CreateEmptyTimeline`, `CreateTimelineFromClips`, `AppendToTimeline`,
`ImportTimelineFromFile` are all **MediaPool methods**, not Project/Timeline methods.
`AppendToTimeline` acts on the *current* timeline — call `proj.SetCurrentTimeline(tl)` first.

## Import assets

- ✅ `mp.ImportMedia([r"C:\path\file.png"])` → list[MediaPoolItem]. Works from absolute paths.
- 🔌 `MediaStorage.AddItemListToMediaPool(itemInfos)` — storage-browser variant, untested.
- 🔌 `mp.ImportFolderFromFile`, `mp.ImportTimelineFromFile` (AAF/EDL/XML/FCPXML/DRT/OTIO —
  with `ImportOptions`), `mp.ImportFolderFromFile` for relinked folder structures.

## Bins / folders

- 🔌 `mp.AddSubFolder(root, "Dailies")`, `SetCurrentFolder`, `MoveClips`, `MoveFolders`,
  `DeleteFolders`, `DeleteClips` (pool-level delete — NOT the same as Timeline.DeleteClips).
- ⚠️ Importing the same file twice creates duplicate pool items. De-dupe by checking
  `root.GetClipList()` for matching `.GetName()` before ImportMedia.

## Clip metadata / properties

- 🔌 `item.GetClipProperty("File Path" / "Type" / ...)`, `item.SetClipProperty(...)`,
  `item.SetClipColor("Green")`, `item.AddMarker(...)`, takes/mattes via methods file.
- 🔌 `mp.ExportMetadata(fileName, clips)` — ALE/CSV metadata out.

## Timelines from clips

- ✅ `mp.CreateTimelineFromClips(name, [{"mediaPoolItem": item}, ...])` — verified 21.1:
  dict key is literally `mediaPoolItem`. Video + embedded audio + separate WAV all land
  on one timeline (2 video clips -> 3 audio clips). Appends sequentially at track end.
- ✅ `mp.CreateEmptyTimeline(name)` then `mp.AppendToTimeline([item])` — verified path.

## Still images (AI-generated assets etc.)

- ✅ PNG imports as clip `Type == "Still"`; default duration ~151 frames at 30fps.
- ✅ Append to a track, then build a Fusion comp on the item (see fusion-comp.md).
- ⚠️ An image clip's Fusion comp contains `MediaIn1` — the image itself is a node; any comp
  you build must end in MediaOut1 or the clip renders black.
