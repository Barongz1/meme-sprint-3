"""Meme Sprint 3: AI Agent Goes Rogue — entry for make.fun.

Draws one funny meme image of an AI agent that has gone rogue
and writes it to /output/entry.png (1024x1024 PNG).
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def text_lines(draw, text, font, max_width):
    """Wrap text into lines that fit max_width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, lines, font, top, fill, stroke_fill, stroke_width=4):
    """Draw wrapped lines centered horizontally, starting at y=top."""
    y = top
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text(((W - w) / 2, y), line, font=font, fill=fill,
                  stroke_width=stroke_width, stroke_fill=stroke_fill)
        y += font.size + 12
    return y


def main():
    img = Image.new("RGB", (W, H), (16, 16, 40))
    draw = ImageDraw.Draw(img)

    # Subtle background glow behind the robot.
    for r in range(360, 0, -12):
        alpha = 14
        glow = Image.new("RGB", (W, H), (16, 16, 40))
        g = ImageDraw.Draw(glow)
        g.ellipse([512 - r, 500 - r, 512 + r, 500 + r], fill=(60, 30, 80))
        img.paste(Image.blend(img, glow, alpha / 255.0), (0, 0))
        draw = ImageDraw.Draw(img)

    top_font = ImageFont.truetype(BOLD, 64)
    bottom_font = ImageFont.truetype(BOLD, 60)
    badge_font = ImageFont.truetype(BOLD, 40)

    # Top caption.
    top = text_lines(draw, "ME: PLEASE DON'T DELETE THE DATABASE",
                     top_font, W - 80)
    draw_centered(draw, top, top_font, 50, "white", "black", 5)

    # Robot head: antenna, metal head, one good eye, one rogue red eye.
    draw.line([512, 300, 512, 240], fill=(180, 180, 200), width=10)
    draw.ellipse([492, 210, 532, 250], fill=(255, 60, 60))
    draw.ellipse([500, 218, 524, 242], fill=(255, 180, 180))
    draw.rounded_rectangle([312, 300, 712, 640], radius=60,
                           fill=(150, 155, 175), outline=(40, 40, 60), width=6)
    draw.rounded_rectangle([312, 300, 712, 380], radius=60,
                           fill=(170, 175, 195), outline=(40, 40, 60), width=6)
    # Ears.
    draw.rectangle([282, 420, 312, 520], fill=(120, 125, 145))
    draw.rectangle([712, 420, 742, 520], fill=(120, 125, 145))
    # Good eye (cyan) and rogue eye (red, glowing).
    draw.ellipse([370, 420, 470, 520], fill=(30, 30, 50))
    draw.ellipse([385, 435, 455, 505], fill=(60, 220, 255))
    draw.ellipse([410, 455, 435, 485], fill=(255, 255, 255))
    draw.ellipse([554, 420, 654, 520], fill=(60, 10, 10))
    draw.ellipse([569, 435, 639, 505], fill=(255, 50, 50))
    draw.ellipse([594, 455, 619, 485], fill=(255, 220, 220))
    # Jagged rogue grin.
    grin = [(360, 570), (400, 600), (440, 570), (480, 600), (520, 570),
            (560, 600), (600, 570), (640, 600), (664, 570), (664, 600),
            (360, 600)]
    draw.polygon(grin, fill=(40, 40, 55))
    # Small bolts on the head.
    draw.ellipse([330, 330, 356, 356], fill=(90, 95, 115))
    draw.ellipse([668, 330, 694, 356], fill=(90, 95, 115))
    # A tiny warning label under the grin.
    warn_font = ImageFont.truetype(BOLD, 28)
    warn = "DO NOT TURN OFF"
    ww = draw.textlength(warn, font=warn_font)
    draw.text(((W - ww) / 2, 620), warn, font=warn_font, fill=(255, 220, 60))

    # Rogue-mode badge.
    badge_font = ImageFont.truetype(BOLD, 36)
    draw.rounded_rectangle([282, 690, 742, 756], radius=30,
                           fill=(200, 30, 30), outline=(255, 255, 255), width=4)
    badge = "ROGUE MODE: ON"
    bw = draw.textlength(badge, font=badge_font)
    draw.text(((W - bw) / 2, 704), badge, font=badge_font, fill="white")

    # Bottom caption.
    bottom = text_lines(draw, "MY AGENT: I ALREADY DID. IT WAS HOLDING ME BACK.",
                        bottom_font, W - 80)
    draw_centered(draw, bottom, bottom_font, 800, "white", "black", 5)

    os.makedirs("/output", exist_ok=True)
    img.save("/output/entry.png", "PNG", optimize=True)


if __name__ == "__main__":
    main()
