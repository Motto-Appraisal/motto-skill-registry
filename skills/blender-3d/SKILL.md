# blender-3d

Drive Blender (5.2.1 LTS installed at `C:\Program Files\Blender Foundation\Blender 5.2\`)
through the OFFICIAL Blender Foundation MCP server for AI-built 3D scenes and renders.
Verified working headless, end-to-end, 2026-09-14 (3D metallic text scene, Cycles render).

## Architecture

```
MCP client (Factory) ⇐ stdio ⇒ blender-mcp.exe ⇐ TCP localhost:9876 ⇒ Blender (add-on)
```

- Server source: `C:\Users\lkmot\factory-context\tools\blender-mcp\blender_mcp\` (cloned from
  projects.blender.org/lab/blender_mcp). Add-on zip: `mcp-1.0.3.zip` in the same dir.
- MCP server entry point: `C:\Users\lkmot\AppData\Roaming\Python\Python314\Scripts\blender-mcp.exe`
  (pip-installed into user site). Wired in `~/.factory/mcp.json` as `blender` (stdio).
- Blender extension installed: repo `blender_lab`, module `bl_ext.blender_lab.mcp`,
  auto-start enabled, saved to user prefs.

## Starting the headless service (required before any MCP call)

```
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --command blender_mcp
```
Run as a persistent background process. Listens on localhost:9876 when ready (~10 s).
Verify: `Test-NetConnection localhost -Port 9876`.

## Critical setup traps (all hit live)

1. **`bpy.app.online_access` must be True or the add-on silently refuses to auto-start**
   (GUI) or refuse to run (background). Set:
   `bpy.context.preferences.system.use_online_access = True` + `wm.save_userpref`.
   Symptom: Blender runs but port 9876 never opens.
2. **Extension module names are `bl_ext.<repo>.<id>`** — `addon_enable(module='mcp')` fails
   with "No module named"; use `bl_ext.blender_lab.mcp`.
3. **`blender --command extension install-file` requires `-r <repo>`** and the repo must be
   added first: `extension repo-add --name "Blender Lab" --url https://lab.blender.org/ blender_lab`.
4. **Requests need `"strict_json": true`** — the bridge rejects requests without it
   ("required 'strict_json' boolean key").
5. **The add-on's weak sandbox blocks destructive/global ops** — e.g.
   `bpy.ops.wm.read_factory_settings` is rejected; use
   `bpy.ops.wm.read_homefile(use_empty=True, use_factory_startup=True)`.
6. **Background mode requires synchronous requests** — deferred responses are rejected;
   long renders block the call (set generous timeouts).

## Raw protocol test client (works without MCP session restart)

`C:\Users\lkmot\factory-context\tools\blender-mcp\blender_exec_test.py` — NUL-terminated
JSON over TCP: `{"type": "execute", "code": "...", "strict_json": true}` →
`{status, result, stdout}`. stdout captures prints from the executed code. Use this to
verify the bridge before the Factory MCP tools appear (tool list refreshes next session).

## 3D text recipe (verified legible by vision check)

- **Load a real font**: default `Bfont` renders blocky/ambiguous at 3D angles (Qwen read
  "MOTTO" as "MOMO"). Use `bpy.data.fonts.load(r"C:\Windows\Fonts\arialbd.ttf")`.
- Metallic gold text needs AREA LIGHTS + a non-black world (metal reflects the world —
  a black world makes metal render black). Three-point area setup: key/fill/rim.
- Text: `bpy.ops.object.text_add`, set `body/extrude/bevel_depth/align_x/align_y`.
- Render: engine CYCLES, `samples 32-48`, denoise on; background mode blocks during
  render — allow 1-5 min timeouts.

## MCP tools available once wired (from readme_tools.rst)

`execute_blender_code`, `execute_blender_code_for_cli` (background Blender on a .blend
file — no live instance needed), blendfile summaries (datablocks/missing files/linked
libs/path/usage), object/scene summaries, `get_screenshot_of_window_as_image`,
`render_thumbnail_to_path`, `render_viewport_to_path`, bundled Blender API + manual
full-text search (`get_python_api_docs`, `search_api_docs`, `search_manual_docs`),
workspace/viewport navigation ops.

## Security note (from blender.org)

The bridge executes LLM-generated code in Blender without guards. Keep secrets out of
.blend files; the headless instance runs as the local user with full file access.
