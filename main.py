#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House: A Letter in One Image.

The invitation itself (a typeset letter over a real photo of the
house, rendered at build time by tools/render_letter.py) ships in
this repository as assets/invitation.png. This entrypoint only
places that shipped image at /output/entry.png, after checking it
against the competition gate with the standard library alone:
a whole PNG, at most 1 MiB and at most 1024 by 1024 pixels.

Usage:
    python3 main.py            # write /output/entry.png
    python3 main.py --check    # validate the asset, write nothing
    python3 main.py --self-test  # write to a temp file, verify bytes
"""

import hashlib
import os
import shutil
import struct
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(HERE, "assets", "invitation.png")
DEST = "/output/entry.png"

MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_png_size(path):
    """Return (width, height) from a PNG header, stdlib only."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if head[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG file: bad signature")
    if head[12:16] != b"IHDR":
        raise ValueError("not a PNG file: missing IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def validate(path):
    """Check the asset against the gate; return (width, height, bytes)."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError(f"image is {size} bytes, over the 1 MiB gate")
    width, height = read_png_size(path)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(
            f"image is {width}x{height}, over the 1024x1024 gate"
        )
    return width, height, size


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_entry(dest):
    width, height, size = validate(ASSET)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copyfile(ASSET, dest)
    # Verify the copy landed intact before reporting success.
    if sha256_of(ASSET) != sha256_of(dest):
        raise ValueError("copy failed: destination hash differs")
    print(f"wrote {dest}: {width}x{height} PNG, {size} bytes")
    print(f"sha256: {sha256_of(dest)}")
    return dest


def self_test():
    """Write to a temp file and verify the bytes round-trip exactly."""
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "entry.png")
        write_entry(out)
        with open(ASSET, "rb") as src, open(out, "rb") as got:
            assert src.read() == got.read(), "bytes differ after copy"
        print("self-test ok: output byte-identical to the asset")


def main(argv):
    if "--check" in argv:
        width, height, size = validate(ASSET)
        print(f"check ok: {width}x{height} PNG, {size} bytes")
        return 0
    if "--self-test" in argv:
        self_test()
        return 0
    write_entry(DEST)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
