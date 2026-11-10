#!/usr/bin/env python3
"""Build SoulWorkerDocs-standalone.html from the SoulWorkerDocs folder source.

The folder version (SoulWorkerDocs.html + data.js + fonts/ + icons/ + vendor/ + icon.png) stays
the source you edit. This script produces the one file you can send to a friend or open from a
USB stick: the payload is gzipped and base64'd into a text block the app inflates at boot, the
spreadsheet library goes in as a second block the app inflates only when a spreadsheet is asked
for, every asset path is swapped for a base64 data URI, and the app's own scripts and style
block are compacted (comments and indentation removed), so the output makes no file or network
reference and reads like a machine file.

Harder to read is not the same as hard to reverse engineer. The browser has to decode and
execute everything in here, so a devtools console still shows window.SW_DATA and the running
code. Treat this as keeping a casual reader out, not a determined one.

Run after any change to the app:  python build_standalone.py
"""

import base64
import gzip
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT / "SoulWorkerDocs.html"
PAYLOAD = ROOT / "data.js"
LIBRARY = ROOT / "vendor" / "xlsx.full.min.js"
LIBRARY_LICENSE = ROOT / "vendor" / "xlsx-LICENSE"
OUTPUT = ROOT / "SoulWorkerDocs-standalone.html"

PAYLOAD_PREFIX = "window.SW_DATA = "
PAYLOAD_ID = "sw-data-b64"
LIBRARY_ID = "sw-xlsx-b64"

DECODE_SNIPPET = """<script id="{pid}" type="text/plain">{b64}</script>
    <script>
    window.SW_DATA = (function () {{
        var bin = atob(document.getElementById('{pid}').textContent);
        var bytes = new Uint8Array(bin.length);
        for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
        var inflated = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
        return new Response(inflated).text().then(JSON.parse);
    }})();
    </script>"""

LIBRARY_SNIPPET = """<script id="{pid}" type="text/plain">{b64}</script>"""

MIME = {
    ".png": "image/png",
    ".woff2": "font/woff2",
    ".woff": "font/woff",
    ".ttf": "font/ttf",
}

# A "/" starts a regex literal only after one of these; after anything else it divides.
REGEX_OK_BEFORE = "(,=:[!&|?{};+-*%~^\n"
REGEX_KEYWORDS = ("return", "typeof", "instanceof", "in", "of", "new", "delete", "void", "case", "do", "else")


def data_uri(path):
    suffix = path.suffix.lower()
    if suffix not in MIME:
        raise SystemExit("unknown asset type: %s" % path)
    return "data:%s;base64,%s" % (MIME[suffix], base64.b64encode(path.read_bytes()).decode("ascii"))


def collect_assets():
    assets = {}
    for folder in ("icons", "fonts"):
        directory = ROOT / folder
        if not directory.is_dir():
            raise SystemExit("missing asset folder: %s" % directory)
        for item in sorted(directory.iterdir()):
            if item.is_file():
                assets[folder + "/" + item.name] = data_uri(item)
    assets["icon.png"] = data_uri(ROOT / "icon.png")
    return assets


def encode_payload():
    """Validate the JSON payload, then gzip and base64 it: 3.0 MB of records becomes
    ~0.4 MB of gzip and ~0.5 MB of text, and none of it is skimmable in an editor.
    mtime=0 keeps the build byte-identical when the data has not changed."""
    raw = PAYLOAD.read_text(encoding="utf-8")
    if not raw.startswith(PAYLOAD_PREFIX) or not raw.rstrip().endswith(";"):
        raise SystemExit("data.js is not the expected `window.SW_DATA = {...};` shape")
    body = raw[len(PAYLOAD_PREFIX):].rstrip()[:-1]
    try:
        json.loads(body)
    except ValueError as exc:
        raise SystemExit("data.js payload is not valid JSON: %s" % exc)
    gz = gzip.compress(body.encode("utf-8"), compresslevel=9, mtime=0)
    if gzip.decompress(gz) != body.encode("utf-8"):
        raise SystemExit("gzip round-trip of the payload did not match - refusing")
    return len(body.encode("utf-8")), gz, base64.b64encode(gz).decode("ascii")


def encode_library():
    """SheetJS as one gzip+base64 text block, the same discipline as the payload: 0.9 MB of
    minified JavaScript would otherwise sit in the file as readable source the app does not run
    until someone exports a spreadsheet. Refuse the build if the copy is missing, or is not
    valid UTF-8 - the app inflates it with a UTF-8 text decode before it runs it, so a byte the
    decoder cannot read would arrive as a replacement character inside library source - or does
    not inflate back to the byte-for-byte vendor file, because a block that inflates to half a
    library reads as a broken Excel export three clicks later, which is not a failure anyone
    would trace back to this script."""
    for required in (LIBRARY, LIBRARY_LICENSE):
        if not required.is_file():
            raise SystemExit("missing %s - the spreadsheet export cannot be built without it"
                             % required)
    raw = LIBRARY.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit("%s is not valid UTF-8: %s" % (LIBRARY.name, exc))
    if text.encode("utf-8") != raw:
        raise SystemExit("%s does not survive a UTF-8 round trip - refusing" % LIBRARY.name)
    gz = gzip.compress(raw, compresslevel=9, mtime=0)
    if gzip.decompress(gz) != raw:
        raise SystemExit("gzip round-trip of the library did not match - refusing")
    b64 = base64.b64encode(gz).decode("ascii")
    if "<" in b64 or ">" in b64:
        raise SystemExit("the library block would break out of its script tag - refusing")
    return len(raw), gz, b64


def scan(text):
    """Walk code once, yielding (kind, start, end) spans. Kind is code, line, block,
    string, template or regex. Only code spans are safe to edit."""
    spans = []
    i, n = 0, len(text)
    prev_sig = "\n"
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if ch == "/" and nxt == "/":
            end = text.find("\n", i)
            end = n if end < 0 else end
            spans.append(("line", i, end))
            i = end
            continue
        if ch == "/" and nxt == "*":
            end = text.find("*/", i + 2)
            end = n if end < 0 else end + 2
            spans.append(("block", i, end))
            i = end
            prev_sig = " "
            continue
        if ch in "\"'":
            end = _string_end(text, i, ch)
            spans.append(("string", i, end))
            i = end
            prev_sig = ch
            continue
        if ch == "`":
            end = _template_end(text, i)
            spans.append(("template", i, end))
            i = end
            prev_sig = "`"
            continue
        if ch == "/" and _regex_allowed(text, i, prev_sig):
            end = _regex_end(text, i)
            spans.append(("regex", i, end))
            i = end
            prev_sig = "/"
            continue
        if ch not in " \t\r\n":
            prev_sig = ch
        i += 1
    spans.append(("code", n, n))
    return spans


def _string_end(text, start, quote):
    i, n = start + 1, len(text)
    while i < n:
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == quote:
            return i + 1
        if text[i] == "\n":
            raise SystemExit("unterminated string at %d in the app source" % start)
        i += 1
    raise SystemExit("unterminated string at %d" % start)


def _template_end(text, start):
    """Backtick to backtick, skipping ${ ... } which may itself hold strings or templates."""
    i, n = start + 1, len(text)
    while i < n:
        ch = text[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "`":
            return i + 1
        if ch == "$" and i + 1 < n and text[i + 1] == "{":
            i = _brace_end(text, i + 1)
            continue
        i += 1
    raise SystemExit("unterminated template literal at %d" % start)


def _brace_end(text, start):
    depth, i, n = 0, start, len(text)
    while i < n:
        ch = text[i]
        if ch in "\"'":
            i = _string_end(text, i, ch)
            continue
        if ch == "`":
            i = _template_end(text, i)
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise SystemExit("unbalanced ${ } at %d" % start)


def _regex_allowed(text, i, prev_sig):
    if prev_sig in REGEX_OK_BEFORE:
        return True
    # The ">" of an arrow function: () => /re/.test(x) starts a literal, the same character
    # after a comparison (a >= b / c) does not. Only the two-character token counts.
    if prev_sig == ">":
        j = i - 1
        while text[j] in " \t\r\n":
            j -= 1
        if j >= 2 and text[j - 1] == "=" and text[j - 2] not in "=!<>":
            return True
    if prev_sig in (" ", ")", "\n", ";", "}", ""):
        word = re.search(r"(\w+)\s*$", text[:i])
        return bool(word) and word.group(1) in REGEX_KEYWORDS
    return False


def _regex_end(text, start):
    i, n, cls = start + 1, len(text), False
    while i < n:
        ch = text[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "\n":
            raise SystemExit("unterminated regex at %d" % start)
        if cls:
            if ch == "]":
                cls = False
        elif ch == "[":
            cls = True
        elif ch == "/":
            while i < n and text[i].isalpha():
                i += 1
            return i
        i += 1
    raise SystemExit("unterminated regex at %d" % start)


def drop_comments(text):
    """Copy everything except the comment spans, tracking how many lines went away."""
    out, cursor, removed = [], 0, 0
    for kind, start, end in scan(text):
        if kind not in ("line", "block"):
            continue
        out.append(text[cursor:start])
        removed += text.count("\n", start, end)
        cursor = end
    out.append(text[cursor:])
    return "".join(out), removed


def _literal_mask(text):
    """True at every offset that sits inside a string, template or regex span. A multi-line
    template's interior is data: its indentation and blank lines must survive compaction."""
    mask = [False] * len(text)
    for kind, start, end in scan(text):
        if kind in ("string", "template", "regex"):
            for i in range(start, end):
                mask[i] = True
    return mask


def strip_layout(text):
    """Cut leading indentation, trailing blanks and empty lines from code only."""
    mask = _literal_mask(text)
    lines, cursor = [], 0
    while cursor <= len(text):
        nl = text.find("\n", cursor)
        end = len(text) if nl < 0 else nl
        lines.append((cursor, end))
        if nl < 0:
            break
        cursor = end + 1

    kept = []
    for start, end in lines:
        body = text[start:end]
        inside = mask[start:end]
        if body and not any(inside) and not body.strip():
            continue  # blank line made purely of code whitespace
        if body and not inside[0]:
            body = body.lstrip(" \t")
            start += len(text[start:end]) - len(body)
            inside = mask[start:start + len(body)]
        if body and inside and not inside[-1]:
            body = body.rstrip(" \t")
        if body:
            kept.append(body)
    return "\n".join(kept)


def drop_css_comments(text):
    """CSS has no // comments, so the JS scanner must not be used here: a base64 data URI can
    hold '//' and would be eaten as a line comment. Quote-aware block comments only."""
    out, i, n, removed = [], 0, len(text), 0
    quote = None
    while i < n:
        ch = text[i]
        if quote:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "\"'":
            quote = ch
            out.append(ch)
            i += 1
            continue
        if text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end < 0:
                raise SystemExit("unterminated CSS comment at %d" % i)
            removed += text.count("\n", i, end)
            i = end + 2
            continue
        out.append(ch)
        i += 1
    return "".join(out), removed


def compact(html):
    """Compact every inline <script> and <style> body; markup and the payload stay as-is.
    A script is refused if compaction would move even one string, template or regex."""
    stats = {"lines": 0, "literals": 0}

    def repl(match):
        tag, attrs, inner = match.group(1), match.group(2), match.group(3)
        if attrs.strip() or PAYLOAD_ID in attrs:
            return match.group(0)
        if tag == "style":
            # Quoted url() values stay on their own line, so per-line layout is safe here.
            text, removed = drop_css_comments(inner)
            stats["lines"] += removed
            return "<%s>%s</%s>" % (tag, strip_layout(text), tag)
        want = literals(inner)
        stats["literals"] += len(want)
        text, removed = drop_comments(inner)
        out = strip_layout(text)
        if literals(text) != want or literals(out) != want:
            lost = [x for x in want if x not in literals(out)]
            raise SystemExit("compacting a script changed %d of %d literals (first: %s)"
                             % (len(lost), len(want), lost[:1]))
        stats["lines"] += removed
        return "<%s>%s</%s>" % (tag, out, tag)

    html = re.sub(r"<(script|style)([^>]*)>([\s\S]*?)</\1>", repl, html)
    return html, stats


def literals(text):
    """Every string/template/regex span, for the before/after equality check."""
    return sorted(text[a:b] for kind, a, b in scan(text)
                  if kind in ("string", "template", "regex"))


def main():
    html = SOURCE.read_text(encoding="utf-8")
    original = len(html.encode("utf-8"))

    # Assets first, while the only text in the file is the app's own: the payload holds
    # 49k item names and must never be touched by a path substitution.
    # Longest keys first so "icon.png" can never eat part of "icons/foo.png".
    assets = collect_assets()
    counts = {}
    for key in sorted(assets, key=len, reverse=True):
        counts[key] = html.count(key)
        html = html.replace(key, assets[key])

    leftover = [key for key, used in counts.items() if used == 0]
    if leftover:
        print("unused assets (not referenced by the html): " + ", ".join(sorted(leftover)))

    marker = '<script src="data.js"></script>'
    if html.count(marker) != 1:
        raise SystemExit("expected exactly one data.js script tag, found %d" % html.count(marker))

    # Checked on the app text alone, minus the one reference about to be inlined: the
    # payload is 49k item names and any path-like substring inside it would be data.
    app_text = html.replace(marker, "")
    for pattern in ('src="icons/', "src='icons/", 'src="icon.png', 'href="icon.png',
                    "url('fonts/", 'url("fonts/', 'src="data.js', 'src="SoulWorkerDocs'):
        if pattern in app_text:
            raise SystemExit("external reference left in the standalone: " + pattern)

    # Compact before the payload is inserted, so the scanner never walks 4 MB of base64.
    # Each script block checks its own literals inside compact().
    html, stats = compact(html)

    payload_bytes, gz, b64 = encode_payload()
    lib_bytes, lib_gz, lib_b64 = encode_library()
    html = html.replace(marker,
                        DECODE_SNIPPET.format(pid=PAYLOAD_ID, b64=b64) + "\n    "
                        + LIBRARY_SNIPPET.format(pid=LIBRARY_ID, b64=lib_b64), 1)
    if html.count('<script id="%s"' % LIBRARY_ID) != 1:
        raise SystemExit("the library block was not inserted exactly once")

    # The folder build's fix-your-data hint is wrong when the payload is inline.
    hint = "Keep <code>data.js</code> in the same folder as this file, then press Retry."
    standalone_hint = ("This file carries its own data, so a damaged copy is the likely cause - "
                       "re-run build_standalone.py or re-download the file, then press Retry.")
    if html.count(hint) != 1:
        raise SystemExit("expected exactly one data.js fix hint, found %d" % html.count(hint))
    html = html.replace(hint, standalone_hint, 1)

    header = "<!-- Generated by build_standalone.py from SoulWorkerDocs.html + data.js + assets. Do not edit. -->\n"
    body = header + html
    # write_bytes, not write_text: text mode would rewrite every \n as \r\n on Windows and
    # the size printed below would not be the size on disk.
    OUTPUT.write_bytes(body.encode("utf-8"))

    print("source html : %10d bytes" % original)
    print("data payload: %10d bytes json -> %d gzip -> %d base64"
          % (payload_bytes, len(gz), len(b64)))
    print("lib block   : %10d bytes js   -> %d gzip -> %d base64"
          % (lib_bytes, len(lib_gz), len(lib_b64)))
    print("standalone  : %10d bytes -> %s" % (len(body.encode("utf-8")), OUTPUT.name))
    print("compacted   : %d comment lines dropped, %d literals checked and preserved"
          % (stats["lines"], stats["literals"]))
    for key in sorted(counts):
        print("  %-34s %d use%s" % (key, counts[key], "" if counts[key] == 1 else "s"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
