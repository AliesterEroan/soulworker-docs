#!/usr/bin/env python3
"""Generate data.js for SoulWorkerDocs.html from the read-only docs/*.txt tables.

The page runs over file:// where fetch/XHR are blocked, so the payload ships as a
classic script assigning window.SW_DATA. Run after any docs/*.txt change:

    PYTHONIOENCODING=utf-8 python build_data.py           # regenerate data.js
    PYTHONIOENCODING=utf-8 python build_data.py --check   # exit 1 if stale
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent / "docs"
OUT = HERE / "data.js"


def read_source(name):
    raw = (DOCS / name).read_bytes()
    return raw.decode("utf-8"), {
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def table_rows(text):
    for line in text.splitlines():
        line = line.rstrip("\r")
        if line and not line.startswith("#"):
            yield line.split("\t")


def parse_items(text):
    columns = ["id", "name", "group", "bag", "stack"]
    rows = []
    for parts in table_rows(text):
        if len(parts) >= 4:
            rows.append(parts[:4] + [parts[4] if len(parts) > 4 else "1"])
    return {"columns": columns, "rows": rows}


def parse_warps(text):
    sections = []
    current = None
    for line in text.splitlines():
        line = line.rstrip("\r")
        if line.startswith("## "):
            title, _, note = line[3:].strip().partition(" -- ")
            current = {"title": title, "note": note, "columns": [], "rows": []}
            sections.append(current)
        elif current is not None and line.startswith("#"):
            if "\t" in line and not current["columns"]:
                current["columns"] = line[1:].strip().split("\t")
        elif current is not None and line.strip():
            current["rows"].append(line.split("\t"))
    return sections


def parse_commands(text):
    commands = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cmd, sep, note = line.partition("  (")
        commands.append({"cmd": cmd.strip(), "note": ("(" + note) if sep else ""})
    return commands


def build():
    items_text, items_meta = read_source("items.txt")
    warps_text, warps_meta = read_source("warps.txt")
    cmds_text, cmds_meta = read_source("cmd sw.txt")
    return {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sources": {"items": items_meta, "warps": warps_meta, "commands": cmds_meta},
        "items": parse_items(items_text),
        "warps": parse_warps(warps_text),
        "commands": parse_commands(cmds_text),
    }


def serialize(data):
    return "window.SW_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"


def check():
    if not OUT.exists():
        print("STALE: data.js missing")
        return 1
    existing = OUT.read_text(encoding="utf-8")
    payload = existing.split("=", 1)[1].strip().rstrip(";")
    old = json.loads(payload)["sources"]
    fresh = build()["sources"]
    stale = [k for k in fresh if fresh[k] != old.get(k)]
    if stale:
        print("STALE: " + ", ".join(stale) + " changed since data.js was generated")
        return 1
    print("OK: data.js matches docs/*.txt")
    return 0


def main():
    if "--check" in sys.argv:
        return check()
    data = build()
    OUT.write_text(serialize(data), encoding="utf-8")
    n_items = len(data["items"]["rows"])
    n_warps = sum(len(s["rows"]) for s in data["warps"])
    print(f"wrote {OUT.name} ({OUT.stat().st_size:,} bytes): "
          f"{n_items:,} items, {n_warps:,} warp rows in {len(data['warps'])} sections, "
          f"{len(data['commands'])} commands")
    return 0


if __name__ == "__main__":
    sys.exit(main())