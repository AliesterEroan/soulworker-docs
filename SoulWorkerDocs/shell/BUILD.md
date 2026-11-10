# SoulWorker Docs — native Windows shell (Tauri)

Turns `SoulWorkerDocs-standalone.html` into `SoulWorker Docs.exe`: an Explorer icon, a taskbar
name, a window with no browser chrome, and nothing to install beside it.

The shell adds one thing the webview cannot do for itself: **Save file** in the Export sheet opens a
real Windows Save dialog and writes the file you chose. Everything else is still the single HTML
file — Tauri wraps it in a WebView2 window and embeds the bytes. No port, no server, no Flask, no
update check; this folder is unrelated to `SoulWorkerLauncher`, which is a different app on a
different stack.

## Files

| path | what it is |
| --- | --- |
| `build_release.py` | builds and stages the frontend, compiles with private source paths remapped, and checks the resulting exe for known private paths. |
| `prepare_frontend.py` | copies the standalone build to `frontend/index.html` and the icons to `src-tauri/icons/`. Refuses a stale or hand-edited standalone. |
| `frontend/index.html` | build output — the standalone, renamed. Never edit; it is overwritten on every run. |
| `src-tauri/Cargo.toml` | crate manifest, release profile tuned for size. Deps: `tauri`, `tauri-plugin-dialog`, `base64`. |
| `src-tauri/tauri.conf.json` | product name, window size, bundle target, icon, `app.withGlobalTauri` (the page needs `window.__TAURI__`). It is `app`, not `build` — v2 moved it, and the 17:05 build failed with `Additional properties are not allowed ('withGlobalTauri' was unexpected)` on `build`. |
| `src-tauri/build.rs` + `src/main.rs` | one window on the bundled page + `save_export`: it opens the native Save dialog and writes only the chosen path. The command accepts no destination path from the page; it returns the chosen path after writing for the status message. No read, delete or execute command. |
| `src-tauri/capabilities/default.json` | grants `core:default` (so the page can invoke at all) and nothing else. Export needs no dialog permission — the dialog and the write both happen inside `save_export` on the Rust side, never through a page-granted capability. |
| `src-tauri/icons/` | `icon.ico` (16–64 px) + `icon.png`, staged from `SoulWorkerDocs/` by the script. |

## Build it

Open a **cmd** window in the `SoulWorkerDocs` folder, then paste this block. It contains no
machine-specific path. Run the same commands in PowerShell if preferred.

```bat
cargo install tauri-cli --version "^2" --locked
python shell\build_release.py
```

`cargo install` is needed once. `build_release.py` regenerates the standalone, stages it, and runs
`cargo tauri build --ci -- --locked` with compiler source-path remapping for this machine's home,
app, Cargo registry and Rust toolchain directories. It rejects the executable if a known private
build root or Windows user-directory prefix remains readable in UTF-8 or UTF-16. The replacements
are virtual `/build/` paths; the script changes no files in those source directories.

Require cached Cargo dependencies with:

```bat
python shell\build_release.py --offline
```

The builder refuses pre-existing `RUSTFLAGS`, `CARGO_ENCODED_RUSTFLAGS` or `CARGO_TARGET_DIR`
overrides rather than silently bypassing its flags or scanning a different output. Running
`cargo tauri build` directly bypasses this remapping and check. Build logs and intermediate
artifacts can still contain private paths; do not distribute the build directory.

**Disk:** the first build measured **1.2 GB in `target/`** (debug symbols and ~400 crate artifacts). Keeping
it makes later builds fast; `cargo clean` reclaims the space and costs a full recompile next time.

Then:

```
shell\src-tauri\target\release\soulworker-docs.exe
shell\src-tauri\target\release\bundle\nsis\SoulWorker Docs_1.0.0_x64-setup.exe
```

The `.exe` runs standalone (double-click, or pin it). The `-setup.exe` is the installer: it copies
the exe, adds Start Menu and uninstall entries, and writes to the current user only — no admin
prompt, nothing in `Program Files`.

Requirements already on this machine: Rust 1.98 with the MSVC toolchain, VS 2022 Build Tools +
Windows SDK 26100, WebView2 runtime (ships with Edge).

## What is honest to know before you build

| | |
| --- | --- |
| **Internet and runtime** | dependencies and bundler tooling can require downloads. The app carries its data and assets for offline use, but the exe requires WebView2; the installer downloads its bootstrapper when needed. App checks do not establish that Windows or WebView2 never contacts the network. |
| **Size** | measured from the 2026-11-10 path-remapped release: exe **4,162,048 B (3.97 MiB)**, NSIS installer **1,991,703 B (1.90 MiB)** — from the unchanged 1,204,836 B standalone (remapping cost the exe −1,536 B and the installer +86 B vs the 2026-11-09 build). The 11-09 light-default build was 4,163,584 B / 1,991,617 B; the 17:17 build was 4,155,904 B / 1,984,207 B from the 1,168,959 B standalone, so the panels and the light default together cost +7,680 B in the exe and +7,410 B in the installer. The earlier 705 KB build was 3,565,568 B / 1,574,149 B, so the library and the dialog plugin together cost about +590 KB in the exe and +410 KB in the installer. |
| **Build paths are remapped** | the 2026-11-10 release was built by `build_release.py`, which remaps the user-profile, app, Cargo-home and rustc-sysroot prefixes to virtual `/build/*` paths during compilation. Scans of the exe, the installer, its decompressed payload and the embedded exe found **0 private build roots** (the 11-09 exe carried 168 readable local Cargo paths); what remains is 168 virtual `/build/cargo\registry\...` strings naming crates, not this machine. The gate is a byte scan in three encodings, and the builder refuses to finish if any known root survives. Build logs and `target/` still contain local paths — distribute the exe or installer, never the build folder. |
| **The records are less readable than the HTML** | the embedded frontend is compressed by Tauri: none of `sw-data-b64`, `H4sI`, `window.SW_DATA`, `DecompressionStream` or the generated-file marker appear in the exe's raw bytes (`check_exe.py`). So it is no longer a hex-editor glance, unlike the standalone. It is still obscurity, not protection: F12 in the running window dumps `window.SW_DATA`, and the asset is recoverable by anyone who means to unpack it. |
| **Icon and name are in the binary** | `RT_GROUP_ICON` + **5 `RT_ICON` images** (16–64 px, from `icon.ico`) and a `RT_VERSION` block carrying `ProductName`/`FileDescription` = `SoulWorker Docs`, `CompanyName` = `AliesterEroan`, `FileVersion` 1.0.0 — measured from the PE, not by looking at it. |
| **Custom rows do not migrate** | saved rows live in WebView2 storage for the `tauri.localhost` origin, not the `file://` origin. In the exe they are separate from what the browser version remembers: **Export** the JSON in the browser, **Import** it once in the exe. |
| **Export: what the shell grants** | Export opens a settings sheet (shelves, whose rows, format, filename); **Save file** there makes one fused `save_export` call: the Rust side opens the native Save dialog and, only if you pick a path there, writes the base64 payload to it. There is no separate write command and no page-named path, so the arbitrary-path grant the split design implied is gone — the page needs only `core:default`, and a script in this window can ask you for a file but cannot write one you did not choose. Verified in a browser over `file://` with a stub standing in for Tauri (`verify22` J1–J10: one call, no path key, cancel costs one call and writes nothing and leaves the sheet open, failure reports the reason); **and in the built exe itself** — the 2026-11-09 click-test (`reports/docsapp-upgrade-20261108/clicktest_exe.js`, 14/14) drove the real "Save As" window with OS keystrokes, and the 2026-11-10 native check of the remapped release (`reports/docsapp-upgrade-20261108/privacy-build-_t6a93wa/native_check.js`, 16/16) drove it again in an isolated WebView2 profile with PID-scoped dialog automation: cancel wrote nothing, a picked path landed a 2,941,301 B CSV with `Saved: <path>` in the statusbar. |
| **Import is a browser file picker feeding a sheet** | `<input type="file">` + `FileReader`, so it needs no permission at all — and the owner confirmed the picker opens in the built exe. The chosen file is read into the Import sheet (detected format, a preview, one destination per part, merge/replace/append); nothing touches the shelves until **Import**. Reads JSON, CSV, TSV, Markdown and Excel; rows it cannot use are listed with a reason and skipped, not fatal. |
| **SmartScreen** | the exe is unsigned, so first run may show "Windows protected your PC" → More info → Run anyway. A paid code-signing certificate is the only cure. |

## Edit the app

Everything visual and every record still lives one level up:

- `SoulWorkerDocs.html` — the app
- `data.js` — the records
- `vendor/xlsx.full.min.js` — SheetJS, gzipped into the standalone; its licence sits beside it
- `make_icon.py` — `icon.png` → `icon.ico`

Change one, then re-run the two `python` lines and `cargo tauri build`. `prepare_frontend.py` compares timestamps and
stops if it would stage an old standalone, so a stale exe needs you to skip a step on purpose.

To change the window, icon list or product name, edit `src-tauri/tauri.conf.json` — then
`cargo tauri build` again. To replace every icon format at once (including the installer bitmap),
run `cargo tauri icon ..\..\icon.png` from `src-tauri`, which overwrites `src-tauri/icons/`.
