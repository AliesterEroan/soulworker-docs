import argparse
import os
from pathlib import Path
import subprocess
import sys

SHELL = Path(__file__).resolve().parent
APP = SHELL.parent
NATIVE = SHELL / "src-tauri"


def build_environment(offline):
    env = os.environ.copy()
    for name in ("RUSTFLAGS", "CARGO_ENCODED_RUSTFLAGS", "CARGO_TARGET_DIR"):
        if env.get(name):
            raise SystemExit(f"Unset {name} before using this release builder.")
    sysroot = Path(subprocess.check_output(
        ["rustc", "--print", "sysroot"], text=True).strip()).resolve()
    roots = [
        (Path.home().resolve(), "/build/home"),
        (APP, "/build/app"),
        (Path(env.get("CARGO_HOME", Path.home() / ".cargo")).resolve(), "/build/cargo"),
        (sysroot, "/build/rust"),
    ]
    flags = []
    for source, destination in roots:
        for spelling in dict.fromkeys((str(source), source.as_posix())):
            flags.append(f"--remap-path-prefix={spelling}={destination}")
    env["CARGO_ENCODED_RUSTFLAGS"] = "\x1f".join(flags)
    if offline:
        env["CARGO_NET_OFFLINE"] = "true"
    return env, roots


def private_path_hits(data, roots):
    probes = {spelling for source, _ in roots
              for spelling in (str(source), source.as_posix())}
    probes.update((":\\Users\\", ":/Users/"))
    lowered = data.lower()
    return sorted(probe for probe in probes if any(
        probe.lower().encode(encoding) in lowered
        for encoding in ("utf-8", "utf-16-le", "utf-16-be")))


def main():
    parser = argparse.ArgumentParser(description="Build the Windows release with private source paths remapped.")
    parser.add_argument("--offline", action="store_true", help="Require cached Cargo dependencies.")
    args = parser.parse_args()
    env, roots = build_environment(args.offline)
    subprocess.run([sys.executable, str(APP / "build_standalone.py")], check=True)
    subprocess.run([sys.executable, str(SHELL / "prepare_frontend.py")], check=True)
    subprocess.run(["cargo", "tauri", "build", "--ci", "--", "--locked"],
                   cwd=NATIVE, env=env, check=True)
    exe = NATIVE / "target" / "release" / "soulworker-docs.exe"
    hits = private_path_hits(exe.read_bytes(), roots)
    if hits:
        raise SystemExit("Release rejected: private build paths remain in the executable.")
    print(f"PASS: no known private build roots in {exe.name} ({exe.stat().st_size:,} bytes).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
