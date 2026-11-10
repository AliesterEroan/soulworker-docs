# SoulWorker Docs

<div align="center">
  <img src="icon.png" alt="SoulWorker Docs Icon" width="128">
</div>

> Item, warp and GM-command records for SoulWorker in one offline file — v1.0.0, with a native Windows shell, verified end to end on this machine.

The app runs locally without an application server or account. Its standalone HTML document carries the records and assets inside itself; the optional `.exe` wraps that document in a WebView2 window and adds a native Save dialog.

---

## 📜 Table of Contents

- [✨ Features](#-features)
- [🚀 Installation](#-installation)
- [📖 Usage](#-usage)
- [⚙️ Settings](#-settings)
- [🏗️ Architecture](#-architecture)
- [🛠️ Technologies Used](#-technologies-used)
- [⚠️ Limitations](#-limitations)
- [🔒 Privacy](#-privacy)
- [📜 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

---

## ✨ Features

### The records
- **49,028 items, 1,084 warp rows and 32 GM commands** — the snapshot dated 2026-11-08, embedded in the build (counts read from the app's own export sheet, not estimated).
- **Click to copy** — any item row copies `/item <id>`, any warp row its teleport, any command its line; the status bar confirms what was copied.
- **`/` filters, headers sort, 100 rows a page** — keyboard-first reading over 50k rows without a scrollbar marathon.

### Reading them comfortably
- **Light is the default theme**, dark one click away; the choice is remembered and a saved dark never flashes light on the next open.
- **An intro on every visit** — loader, welcome, mascot — matching the project's navigation page, with a per-section error screen if a record shelf is missing.

### Export and Import as settings sheets
- **Export** decides the whole file before anything is written: which shelves, whose rows (yours, or yours plus the game records), one of **six formats** (JSON, CSV, TSV, Markdown, aligned Text, Excel), and the file name — with a live row count and a per-format note on what each format keeps or loses.
- **Import** reads JSON, CSV, TSV, Markdown and Excel, then shows what it made of the file — a preview and one destination per part — before anything touches your rows. Merge, replace or append; rows it cannot use are listed with a reason and skipped, never fatal.
- **Nothing is one-click**: both are overlay dialogs over the docs, so a stray click can never overwrite a file or a shelf.

### The Windows shell
- **`soulworker-docs.exe`** — its own Explorer icon, taskbar name and window, no browser chrome, nothing to install beside it (an NSIS installer is built too, current-user only).
- **Export's "Save file" opens the native Windows Save dialog** and writes only the path you pick in it. `save_export` in `shell/src-tauri/src/main.rs` combines the dialog and write, then returns the chosen path for the status message; the page cannot supply an arbitrary destination path to that command.

---

## 🚀 Installation

### Prerequisites
- **For the exe:** Windows 10/11 x64 and the WebView2 runtime (it ships with Microsoft Edge).
- **For the browser route:** any modern browser; the standalone file needs nothing beside itself.
- **To build from source:** Python 3 (the scripts were run on 3.14), Rust 1.98 with the MSVC toolchain, VS 2022 Build Tools with a Windows SDK, and an internet connection **during the build only**.

### Steps — run the built exe
1. Take `shell/src-tauri/target/release/soulworker-docs.exe`, or the installer `shell/src-tauri/target/release/bundle/nsis/SoulWorker Docs_1.0.0_x64-setup.exe`.
2. Double-click it. First run may show SmartScreen's "Windows protected your PC" because the exe is unsigned — *More info* → *Run anyway*. A paid code-signing certificate is the only cure.
3. Press Enter through the intro.

### Steps — run it in a browser
1. Open `SoulWorkerDocs-standalone.html` — one file, records and spreadsheet library embedded.
2. Or open `SoulWorkerDocs.html` with `data.js` kept in the same folder; the app says so on its error screen if it is missing.

### Steps — build from source
Open **cmd** or PowerShell in the `SoulWorkerDocs` folder, then run:

Install the Tauri CLI once, then use the release builder:

```bat
cargo install tauri-cli --version "^2" --locked
python shell\build_release.py
```

`build_release.py` rebuilds and stages the standalone, compiles with locked dependencies and remapped source paths, and rejects an exe containing known private build roots. Add `--offline` to require cached Cargo dependencies. Running `cargo tauri build` directly bypasses this privacy check. The first build takes a few minutes; `shell/BUILD.md` lists prerequisites and output locations.

---

## 📖 Usage

### Read and copy
1. Press Enter through the intro; the Home page lists the shelves with their counts.
2. Open **Items**, **Warps** or **Commands**; press `/` and type to filter, click a header to sort.
3. Click a row to copy its line — the status bar shows what landed in the clipboard.

### Keep your own rows
1. Press **Edit**, then **Add** (or click a custom row to change it). Custom rows live in this browser's storage only.
2. They appear in the tables with the same sorting and filtering, and in every export you tick them into.

### Export a file
1. Press **Export**. The sheet opens over the docs and writes nothing yet.
2. Tick shelves, choose whose rows, pick a format and a name — the sheet counts the rows live and says what the format keeps or loses.
3. Press **Save file**. In the exe the native Save dialog appears and the file lands where you pick; in a browser the file goes to the downloads folder. Cancel anywhere and nothing is written.

### Import a file back
1. Press **Import**, then **Choose file**.
2. Read what the app made of it: the detected kind, a preview, one destination per part, and how merge/replace/append would treat the rows you already have.
3. Press **Import** — or **Cancel**, which changes nothing. Unusable rows are listed with a reason and skipped.

### Move your rows between the browser and the exe
They are separate storage origins, so custom rows do not travel on their own: **Export** the JSON in one, **Import** it once in the other.

---

## ⚙️ Settings

There is no settings page; the app remembers what you chose, per browser or per exe.

### Available Settings
- **Theme** - button in the toolbar (default: **light**) — stored as `swdocs-theme`; a stored `dark` wins on the next open.
- **Export format** - card in the Export sheet (default: `json`) — one of json/csv/tsv/md/txt/xlsx, remembered in `swdocs-io`.
- **Export shelves** - checkboxes in the Export sheet (default: all three on) — items, warps, commands; remembered in `swdocs-io`.
- **Whose rows** - radio in the Export sheet (default: your own) — yours, or yours plus the read-only game records; remembered in `swdocs-io`.
- **Import mode** - radio in the Import sheet (default: `merge`) — merge by id, replace everything, or append as-is; remembered in `swdocs-io`.
- **Last tab, page size, sort** - remembered in `swdocs-ui` so the app reopens where you left it.
- **First-visit tip** - shown once per origin, recorded in `swdocs-tips`; the intro itself plays on every open by design.

---

## 🏗️ Architecture

```
SoulWorkerDocs/
├── SoulWorkerDocs.html        # the app: styles, markup and every behaviour in one classic-script file
├── SoulWorkerDocs-standalone.html  # build output: the app + gzipped records + SheetJS, one portable file
├── data.js                    # the records as JS (generated; the folder build reads it)
├── build_data.py              # ../docs/ -> data.js
├── build_standalone.py        # app + data.js + vendor -> the standalone, gzip + base64
├── make_icon.py               # icon.png -> icon.ico
├── fonts/                     # self-hosted Plus Jakarta Sans and JetBrains Mono (woff2)
├── icons/                     # toolbar and panel glyphs (icons8 cotton style)
├── vendor/                    # SheetJS xlsx.full.min.js + its Apache-2.0 licence
└── shell/                     # the Tauri v2 Windows shell (see shell/BUILD.md)
    ├── build_release.py       # builds with compiler path remapping and checks the resulting exe
    ├── prepare_frontend.py    # stages the standalone + icons; refuses a stale standalone
    ├── frontend/index.html    # build output, byte-identical to the standalone
    └── src-tauri/
        ├── src/main.rs        # one window + save_export: native Save dialog, then write the picked path
        ├── capabilities/default.json  # core:default and nothing else
        └── tauri.conf.json    # product name, window, bundle, icon, app.withGlobalTauri
```

### Component Overview
- **`SoulWorkerDocs.html`** - everything visual and every record interaction; the intro, the tables, the editor, and the Export/Import sheets.
- **`build_standalone.py`** - inlines `data.js` as a gzip+base64 block and SheetJS as a second lazy one, so the standalone stays a single file.
- **`shell/src-tauri/src/main.rs`** - `save_export(name, label, ext, data)`: opens the native Save dialog on a worker thread and, only if a path comes back, writes the base64 payload there. Cancel returns nothing and writes nothing.

### Data Flow
1. `../docs/` → `build_data.py` → `data.js` (the snapshot, with its generation date).
2. `data.js` + `SoulWorkerDocs.html` + `vendor/` → `build_standalone.py` → the standalone, records compressed.
3. At boot the page inflates the records once (SheetJS only when an Excel file is touched), renders the tables, and replays the intro.
4. Export: the sheet's choices → one of six writers → bytes → `save_export` (exe) or a download (browser).
5. Import: a chosen file → parsed once → per-part destinations → merge/replace/append into your rows.

---

## 🛠️ Technologies Used

### Core
- **Vanilla HTML, CSS and JavaScript in one file** - the app is a portable document, not a deployed site; a framework build step was rejected because it would break that promise.
- **Python 3 build scripts** - data and standalone generation; no runtime dependency on Python.

### Shell
- **Tauri v2 + WebView2** - a real window around the same HTML; Electron was rejected on install size and permission surface.
- **One fused Rust command** (`save_export`) - dialog and write together, which is what lets the window run on `core:default` alone.

### Libraries and assets
- **SheetJS 0.20.3** (Apache-2.0), vendored - Excel in and out; the npm `xlsx` distribution was rejected as stale, this one came from the project's own CDN.
- **Plus Jakarta Sans and JetBrains Mono** (SIL Open Font License 1.1), self-hosted as woff2 - the pinned type pairing of the design system.
- **DeepTrace Duotone** design tokens - light and dark share one accent set; light is the default.

---

## ⚠️ Limitations

### Records
- **A snapshot, not live data** - the tables are dated 2026-11-08 and do not follow game patches; regenerating them is a separate data task.
- **Fan compilation** - the records belong to the game's owners; this app only reads and re-exports them.

### Platform
- **Custom rows are per origin** - the browser and the exe keep separate storage, so rows added in one are invisible in the other until you Export/Import the JSON.
- **The exe is unsigned** - SmartScreen will warn on first run.
- **The exe's embedded records are compressed, not encrypted** - they can be extracted or read through the running app. Compression does not hide build paths elsewhere in the binary.

### Performance
- **Excel export of all 50,144 rows takes about a second** - the sheet says so before you press Save; the other five formats are immediate.

### Testing Limitations
- **Verified:** 516 automated checks in a headless browser over `file://` (the `verify*.js` suites under `../reports/docsapp-upgrade-20261108/`), and a 14/14 scripted click-test of the built exe that drove the real native Save dialog — cancel wrote nothing, save wrote a 2,941,301-byte CSV.
- **What a clone can re-check:** the browser suites, with Node and a headless Edge; they need no account and no network.
- **What a clone cannot re-check:** the exe click-test without first building the exe (Rust toolchain, ~1.2 GB of `target/`) on a Windows desktop session, because the native Save dialog is a real OS window.
- **Public repo scope:** the published repository ships the app and the `../docs/` source records. The `verify*.js` suites, click-test drivers and report paths cited above stay in the author's local toolkit and are not part of the public repo.

---

## 🔒 Privacy

The app embeds its records and assets for offline use. Browser checks on 2026-11-10 observed no HTTP(S) requests in the tested flows; a static review found no network calls in the first-party app scripts. These checks do not establish that Windows or WebView2 never makes a connection.

- **Local state:** `SoulWorkerDocs.html` stores custom rows and preferences in localStorage. The browser or WebView2 also maintains its own profile and cache. Copying the exe does not copy that saved state.
- **Selected files and clipboard:** imports read a chosen file; exports use the native Save dialog or browser downloads. Clicking a record writes its command to the clipboard.
- **Runtime prerequisite:** the exe requires WebView2. `shell/src-tauri/tauri.conf.json` configures the installer to download its bootstrapper when needed. Builds can also require internet access for dependencies and tooling.
- **No isolation guarantee:** the native capability file grants `core:default`, but this is not an operating-system sandbox. The shell configuration sets `csp` to `null`; no content-security policy blocks outgoing requests.
- **Build paths are remapped (measured 2026-11-10):** the release exe is built by `shell/build_release.py`, which remaps the compiler's local build roots to virtual `/build/*` paths. A byte scan (UTF-8 and UTF-16) of the exe, the NSIS installer, the decompressed installer payload and the embedded exe found **0 private build-machine paths** — down from 168 distinct readable local Cargo-source paths in the 2026-11-09 build. 168 virtual `/build/cargo\registry\...` crate paths remain in the exe; they name crates, not this machine. The remapped exe passed a 16/16 native click-test in an isolated WebView2 profile (`../reports/docsapp-upgrade-20261108/privacy-build-_t6a93wa/`). Build logs and `target/` still contain local paths: distribute only the exe or the installer, never the source/build folder.

---

## 📜 License

SoulWorker Docs is proprietary software — see [LICENSE](LICENSE) for the full terms.

**Copyright © 2026 AliesterEroan. All rights reserved.**

Personal, non-commercial use is permitted; commercial use, redistribution, modification and sublicensing are not, without explicit written permission. The copyright holder's own copies — including the exe handed to friends — travel under those terms. Bundled third-party components (SheetJS, the two fonts, the icon set) stay under their own licenses, listed in the LICENSE file.

---

## 🙏 Acknowledgments

### Libraries and fonts
- **[SheetJS](https://sheetjs.com/)** by SheetJS LLC - the spreadsheet reader/writer behind Excel import and export (Apache License 2.0).
- **[Plus Jakarta Sans](https://github.com/tokotype/PlusJakartaSans)** by Tokotype and **[JetBrains Mono](https://github.com/JetBrains/JetBrainsMono)** by JetBrains - the app's two typefaces (SIL Open Font License 1.1).

### Icons
- **[icons8](https://icons8.com/)** - the cotton-style glyphs in the toolbar and panels, used under the icons8 free license and attributed on the app's Credits page.

### Records
- **SoulWorker** and its item, warp and command data belong to the game's respective owners; the tables here are a fan-made snapshot for personal reference.

Everything else in this folder — the app, the sheets, the shell and the build scripts — is original work.

---

*Built with ❤️ by AliesterEroan*
