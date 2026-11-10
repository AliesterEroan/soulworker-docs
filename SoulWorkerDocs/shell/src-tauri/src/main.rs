// SoulWorker Docs - native shell.
//
// The application is frontend/index.html, staged by shell/prepare_frontend.py from
// SoulWorkerDocs/SoulWorkerDocs-standalone.html. It renders and stores everything itself. What it
// cannot do inside a webview is put up a Windows Save dialog and write the chosen file, so the
// shell does both in one command: save_export opens the dialog, and writes only the path you
// picked in it.
//
// Fusing the two matters more than it looks. Held apart, the page asked the dialog for a path and
// then handed that path to a writer, which meant the window needed a permission to name any file
// on disk - a silent write, no dialog, to anywhere the user's own rights reach. Now no path ever
// exists before you choose one, so the page has no dialog permission at all and only core:default.
// What is left: the dialog itself is reachable from page code, so a script in this window can ask
// you for a file to overwrite as many times as it likes. Nothing here reads, deletes or executes.

// Release builds are windowed apps: no console window behind the docs.
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use base64::Engine as _;
use tauri_plugin_dialog::DialogExt;

/// Asks where to save, then writes there. `name`/`label`/`ext` only pre-fill and filter the
/// dialog - the picked path wins. `data` is the file's bytes in base64, because IPC has no byte
/// type. Ok(None) means the dialog was closed without a choice, so nothing was written.
#[tauri::command]
async fn save_export(
    app: tauri::AppHandle,
    name: String,
    label: String,
    ext: String,
    data: String,
) -> Result<Option<String>, String> {
    // Commands without async run on the main thread, and a blocking dialog on the main thread
    // deadlocks against the event loop that is feeding it. So the dialog goes to a worker.
    let picked = tauri::async_runtime::spawn_blocking(move || {
        app.dialog()
            .file()
            .set_file_name(name)
            .add_filter(label, &[ext.as_str()])
            .blocking_save_file()
    })
    .await
    .map_err(|e| e.to_string())?;

    let Some(picked) = picked else {
        return Ok(None);
    };
    let path = picked.into_path().map_err(|e| e.to_string())?;
    let bytes = base64::engine::general_purpose::STANDARD
        .decode(&data)
        .map_err(|e| format!("the export payload is not base64: {e}"))?;
    std::fs::write(&path, &bytes).map_err(|e| format!("{}: {e}", path.display()))?;
    Ok(Some(path.display().to_string()))
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![save_export])
        .run(tauri::generate_context!())
        .expect("SoulWorker Docs failed to start");
}
