"""Extract embedded data-URI images from an HTML file into separate files.

Finds every `data:image/...` URI in the HTML (in <img src>, srcset, inline
styles, and <style> blocks), writes each image to an images folder, and saves
a copy of the HTML that references those files instead. The input file is
never modified. Identical images are written once and shared.

Usage:
    python scripts/extract_images.py source/page.html
    python scripts/extract_images.py source/page.html --out-dir source/page --images-dir images

By default this writes source/page_extracted.html and source/page_images/.
"""

import argparse
import base64
import hashlib
import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import unquote_to_bytes

EXTENSIONS = {
    "png": "png",
    "jpeg": "jpg",
    "jpg": "jpg",
    "gif": "gif",
    "webp": "webp",
    "svg+xml": "svg",
    "bmp": "bmp",
    "x-icon": "ico",
    "vnd.microsoft.icon": "ico",
    "avif": "avif",
    "tiff": "tif",
}

# data:image/<type>[;params][;base64],  (the payload is found by find_payload_end)
DATA_URI = re.compile(
    r"data:image/(?P<type>[\w.+-]+)(?P<params>(?:;[\w-]+(?:=[^;,\"')\s]*)?)*?)(?P<b64>;base64)?,",
    re.IGNORECASE,
)
# Base64 payloads may be wrapped across lines but never contain spaces,
# so a srcset descriptor like " 2x" is not swallowed.
BASE64_PAYLOAD = re.compile(r"[A-Za-z0-9+/=\r\n]*")
# Matches alt="..." in normal tags and alt=&quot;...&quot; in HTML-escaped
# markup (for example, pages stored in an iframe's srcdoc attribute).
ALT = re.compile(r"""\balt\s*=\s*(["']|&quot;|&#39;)(.*?)\1""", re.IGNORECASE | re.DOTALL)


def slugify(text, max_len=40):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len].rstrip("-")


def alt_text_for(html, pos):
    """Return the alt text of the <img> tag containing position `pos`, if any."""
    plain, escaped = html.rfind("<", 0, pos), html.rfind("&lt;", 0, pos)
    if escaped > plain:
        start, opener, closer = escaped, "&lt;img", "&gt;"
    else:
        start, opener, closer = plain, "<img", ">"
    if start == -1 or html[start:start + len(opener)].lower() != opener:
        return ""
    end = html.find(closer, pos)
    match = ALT.search(html, start, end if end != -1 else len(html))
    if not match:
        return ""
    # Escaped markup can be escaped more than once (&amp;amp;).
    text = match.group(2)
    for _ in range(3):
        text = unescape(text)
    return text


def find_payload_end(html, match):
    """Return the index where the data URI's payload ends."""
    start = match.end()
    if match.group("b64"):
        return BASE64_PAYLOAD.match(html, start).end()
    # Plain (URL-encoded or raw) payloads such as SVG can contain spaces and
    # quotes, so end at whatever delimiter opened the URI.
    opener = html[match.start() - 1] if match.start() else ""
    closer = {'"': '"', "'": "'", "(": ")"}.get(opener)
    if closer:
        end = html.find(closer, start)
        return end if end != -1 else len(html)
    stop = re.compile(r"[\s\"'<>]").search(html, start)
    return stop.start() if stop else len(html)


def decode(match, payload):
    if match.group("b64"):
        payload = re.sub(r"\s+", "", payload)
        payload += "=" * (-len(payload) % 4)
        return base64.b64decode(payload, validate=True)
    return unquote_to_bytes(payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("html", type=Path, help="HTML file containing embedded images")
    parser.add_argument("--out-dir", type=Path, help="Folder for the output HTML and images (default: next to the input)")
    parser.add_argument("--images-dir", help="Name of the images subfolder (default: <name>_images)")
    parser.add_argument("--output", help="Output HTML filename (default: <name>_extracted.html)")
    parser.add_argument("--prefix", default="image", help="Filename prefix for images without alt text")
    args = parser.parse_args()

    src = args.html
    if not src.is_file():
        sys.exit(f"Not found: {src}")

    out_dir = args.out_dir or src.parent
    images_name = args.images_dir or f"{src.stem}_images"
    images_dir = out_dir / images_name
    out_html = out_dir / (args.output or f"{src.stem}_extracted.html")
    if out_html.resolve() == src.resolve():
        sys.exit("Output HTML would overwrite the input; choose a different --output.")

    html = src.read_text(encoding="utf-8", errors="surrogateescape")
    images_dir.mkdir(parents=True, exist_ok=True)

    by_hash = {}      # sha1 -> relative path already written
    used_names = set()
    counter = 0
    failures = 0

    def replace(match, payload):
        nonlocal counter, failures
        try:
            data = decode(match, payload)
        except ValueError as err:  # includes binascii.Error from bad base64
            failures += 1
            print(f"  skipped an image at offset {match.start()}: {err}", file=sys.stderr)
            return None

        digest = hashlib.sha1(data).hexdigest()
        if digest in by_hash:
            return by_hash[digest]

        counter += 1
        ext = EXTENSIONS.get(match.group("type").lower(), match.group("type").lower())
        base = slugify(alt_text_for(html, match.start())) or args.prefix
        name = f"{counter:03d}-{base}.{ext}"
        while name in used_names:
            counter += 1
            name = f"{counter:03d}-{base}.{ext}"
        used_names.add(name)

        (images_dir / name).write_bytes(data)
        rel = f"{images_name}/{name}"
        by_hash[digest] = rel
        print(f"  {rel}  ({len(data) / 1024:.1f} KB)")
        return rel

    print(f"Extracting images from {src}")
    parts = []
    pos = 0
    for match in DATA_URI.finditer(html):
        if match.start() < pos:  # inside a payload already consumed
            continue
        end = find_payload_end(html, match)
        payload = html[match.end():end]
        if not payload.strip():
            continue
        rel = replace(match, payload)
        if rel is None:
            continue
        # Keep a trailing line break from a wrapped base64 payload.
        trailing = payload[len(payload.rstrip()):]
        parts.append(html[pos:match.start()])
        parts.append(rel + trailing)
        pos = end
    parts.append(html[pos:])
    new_html = "".join(parts)
    out_html.write_text(new_html, encoding="utf-8", errors="surrogateescape")

    print(
        f"\nWrote {len(by_hash)} image(s) to {images_dir}"
        f"\nWrote {out_html} ({len(new_html) / 1024:.0f} KB, was {len(html) / 1024:.0f} KB)"
    )
    if failures:
        print(f"{failures} image(s) could not be decoded and were left embedded.", file=sys.stderr)


if __name__ == "__main__":
    main()
