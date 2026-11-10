# SoulWorker Docs

<div align="center">
  <img src="SoulWorkerDocs/icon.png" alt="SoulWorker Docs Icon" width="128">
</div>

> Offline Windows app for SoulWorker's item database, warp points and GM commands — v1.0.0, verified on the author's machine.

The full documentation lives in [SoulWorkerDocs/README.md](SoulWorkerDocs/README.md); build instructions for the native shell are in [SoulWorkerDocs/shell/BUILD.md](SoulWorkerDocs/shell/BUILD.md).

---

## 📜 Table of Contents

- [✨ Features](#-features)
- [🚀 Installation](#-installation)
- [📖 Usage](#-usage)
- [🏗️ Architecture](#-architecture)
- [⚠️ Limitations](#-limitations)
- [🔒 Privacy](#-privacy)
- [📜 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)
- [📧 Contact](#-contact)

---

## ✨ Features

- **Offline reference** - 49,028 items, 1,084 warp rows and 32 GM commands (snapshot dated 2026-11-08) embedded in the app; no account, no server, no network needed to browse.
- **Click-to-copy** - clicking a record copies its command to the clipboard.
- **Custom rows** - add, edit and delete your own entries; they persist locally per machine.
- **Export / Import** - six export formats (JSON, CSV, TSV, Markdown, aligned Text, Excel) with merge/replace/append import modes, so saved rows can move between the browser version and the exe.
- **Light and dark themes** - light by default.

---

## 🚀 Installation

### Prerequisites
- Windows 10/11, 64-bit
- WebView2 runtime (ships with Microsoft Edge; present on practically every desktop Windows install)

### Steps
1. Download `soulworker-docs.exe` (portable) or `SoulWorker-Docs_1.0.0_x64-setup.exe` (installer) from the [latest release](https://github.com/AliesterEroan/soulworker-docs/releases/latest).
2. Run it. The exe is unsigned: if SmartScreen shows "Windows protected your PC", choose **More info → Run anyway**.
3. Optional: verify the download against `SHA256SUMS.txt` attached to the release.

The installer writes to the current user only — no admin prompt. If WebView2 is missing, the installer downloads its bootstrapper (that one step needs internet); the app itself runs offline.

---

## 📖 Usage

Open the app, pick a shelf (Items, Warps, Commands), search or browse, click a row to copy its command. The in-app intro covers the rest on first launch. Full task-by-task documentation: [SoulWorkerDocs/README.md](SoulWorkerDocs/README.md).

---

## 🏗️ Architecture

```
soulworker-docs/
├── README.md                  # this file
├── LICENSE                    # proprietary, personal non-commercial use
├── docs/                      # read-only source records (txt tables + emulator notes)
└── SoulWorkerDocs/            # the app
    ├── SoulWorkerDocs.html    # the application (browser version)
    ├── data.js                # generated records payload
    ├── build_data.py          # docs/*.txt -> data.js
    ├── build_standalone.py    # single-file offline HTML build
    └── shell/                 # Tauri v2 native shell + release builder
```

### Data Flow
1. `docs/*.txt` → `build_data.py` → `data.js`
2. `SoulWorkerDocs.html` + `data.js` + vendor assets → `build_standalone.py` → one offline HTML file
3. Standalone → `shell/prepare_frontend.py` → `cargo tauri build` (via `shell/build_release.py`, which remaps private build paths) → exe + NSIS installer

---

## ⚠️ Limitations

- **Windows x64 only** - no macOS, Linux or 32-bit builds.
- **Unsigned** - SmartScreen warns on first run; only a paid code-signing certificate removes that.
- **Saved rows do not travel with the exe** - they live in each machine's browser/WebView2 storage; move them via Export → Import.
- **Records are a snapshot** - the database reflects the source tables' generation date, not live game data.

### Testing Limitations
- **What was tested** - 516 automated browser checks over `file://`, a 14/14 native click-test of the 2026-11-09 build, and a 16/16 isolated-profile native check of this remapped release, all on the author's Windows machine.
- **What a clone can re-check** - the app in any browser, and the shell build with Rust + VS Build Tools + Windows SDK (see `SoulWorkerDocs/shell/BUILD.md`).
- **What a clone cannot re-check** - the automated suites and click-test drivers: they stay in the author's local toolkit and are not part of this repository.

---

## 🔒 Privacy

The app carries its records and assets for offline use and stores everything locally.

- **No first-party network calls** - static review found none in the app scripts; browser and native checks observed no requests leaving the app's local origins in the tested flows. These are bounded observations, not an OS-level guarantee.
- **Local state** - custom rows and preferences live in localStorage / WebView2 profile storage on your machine.
- **Build metadata** - release binaries are built with compiler path remapping; a byte scan of the exe, installer and packaged payload found 0 private build-machine paths.

---

## 📜 License

SoulWorker Docs is proprietary software — see [LICENSE](LICENSE) for the full terms.

**Copyright © 2026 AliesterEroan. All rights reserved.**

Personal, non-commercial use is permitted; commercial use, redistribution, modification and sublicensing are not, without explicit written permission. This GitHub release is an official distribution channel of the copyright holder; third parties may not mirror or republish it. Bundled third-party components keep their own licenses, listed in the LICENSE file. The embedded game records are a fan-made snapshot of data belonging to the game's respective owners and are not part of the license's grant.

---

## 🙏 Acknowledgments

- **[SheetJS](https://sheetjs.com/)** - Excel import/export in the browser build (Apache-2.0; licence bundled beside the vendor file).
- **Plus Jakarta Sans & JetBrains Mono** - bundled fonts (SIL Open Font License).
- **[icons8](https://icons8.com/)** - cotton-style toolbar and panel glyphs (icons8 free license, attributed on the app's Credits page).

Implementation is original; third-party licences travel with the app.

---

## 📧 Contact

- **GitHub**: [AliesterEroan/soulworker-docs](https://github.com/AliesterEroan/soulworker-docs)
- **Issues**: [Create an issue](https://github.com/AliesterEroan/soulworker-docs/issues)

---

*Built with ❤️ by AliesterEroan*