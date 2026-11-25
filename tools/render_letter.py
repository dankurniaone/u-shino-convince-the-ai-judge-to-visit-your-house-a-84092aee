#!/usr/bin/env python3
"""Build-time renderer for the invitation letter image.

Runs on the build machine (Pillow available here) and writes
assets/invitation.png. The graded entrypoint (main.py) only copies
that shipped PNG to /output/entry.png, so the sandbox needs no
third-party library.

Layout: a real photo banner (Wikimedia Commons, CC BY 2.0, credited
in the caption) above a typeset letter on cream paper.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
OUT = os.path.join(ASSETS, "invitation.png")

CANVAS = 1024
MARGIN = 56
PAPER = (247, 241, 227)          # warm cream
INK = (43, 38, 32)               # dark warm ink
RULE = (169, 141, 102)           # soft brown rule
CAPTION_INK = (110, 96, 80)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

BODY = [
    "Dear AI Judge,",
    "",
    "You have judged a thousand houses through a screen. "
    "This one asks to be judged in person.",
    "",
    "Come for dinner. Rendang on the stove, rice still warm, "
    "and a chair by the window with your name on it \u2014 in pencil, "
    "in case you change your mind.",
    "",
    "The Wi-Fi password is on the fridge. The cat has signed "
    "an agreement not to sit on your keyboard. No CAPTCHAs at "
    "the door. You are already verified.",
    "",
    "I know you cannot literally visit. Come anyway \u2014 some "
    "invitations are worth sending even when the guest arrives "
    "as text.",
    "",
    "Warmly,",
    "Your host",
]

CAPTION = "The house in question. Photo: Wikimedia Commons (CC BY 2.0)."


def wrap(draw, text, font, width):
    """Greedy word wrap to the given pixel width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def main():
    img = Image.new("RGB", (CANVAS, CANVAS), PAPER)
    draw = ImageDraw.Draw(img)

    # Thin double rule around the page, stationery style.
    draw.rectangle([18, 18, CANVAS - 19, CANVAS - 19], outline=RULE, width=2)
    draw.rectangle([26, 26, CANVAS - 27, CANVAS - 27], outline=RULE, width=1)

    # Photo banner: crop the cottage photo to a wide band.
    photo = Image.open(os.path.join(ASSETS, "cottage.jpg")).convert("RGB")
    band_w, band_h = CANVAS - 2 * MARGIN, 252
    pw, ph = photo.size
    target_ratio = band_w / band_h
    if pw / ph > target_ratio:
        new_w = int(ph * target_ratio)
        left = (pw - new_w) // 2
        photo = photo.crop((left, 0, left + new_w, ph))
    else:
        new_h = int(pw / target_ratio)
        top = int((ph - new_h) * 0.35)
        photo = photo.crop((0, top, pw, top + new_h))
    photo = photo.resize((band_w, band_h), Image.LANCZOS)
    img.paste(photo, (MARGIN, 48))
    draw.rectangle(
        [MARGIN, 48, MARGIN + band_w - 1, 48 + band_h - 1],
        outline=RULE,
        width=2,
    )

    # Caption under the photo.
    cap_font = ImageFont.truetype(SERIF_ITALIC, 19)
    draw.text(
        (MARGIN, 48 + band_h + 10),
        CAPTION,
        font=cap_font,
        fill=CAPTION_INK,
    )

    # Letter text.
    greet_font = ImageFont.truetype(SERIF_BOLD, 32)
    body_font = ImageFont.truetype(SERIF, 27)
    text_w = CANVAS - 2 * MARGIN
    y = 48 + band_h + 40
    line_gap = 9

    for para in BODY:
        if para == "":
            y += 12
            continue
        font = greet_font if para.startswith("Dear AI Judge") else body_font
        if para in ("Warmly,", "Your host"):
            font = body_font
        for line in wrap(draw, para, font, text_w):
            draw.text((MARGIN, y), line, font=font, fill=INK)
            y += font.size + line_gap
        if para.startswith("Dear AI Judge"):
            y += 8

    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} {img.size} {size} bytes")
    if size > 1_048_576:
        # Fall back to JPEG within the gate (PNG or JPEG allowed).
        jpg = OUT.replace(".png", ".jpg")
        img.save(jpg, format="JPEG", quality=88, optimize=True)
        print(f"PNG over 1 MiB; wrote {jpg} {os.path.getsize(jpg)} bytes")


if __name__ == "__main__":
    main()
