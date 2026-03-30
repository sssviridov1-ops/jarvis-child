#!/usr/bin/env python3
"""
Генератор карусели PNG в стиле Сергея Свиридова:
тёмный фон #080808, белый текст Montserrat/системный шрифт.

Использование:
  python3 carousel_gen.py "Слайд 1\n---\nСлайд 2\n---\nСлайд 3"

Возвращает список путей к PNG-файлам.
"""

import os
import sys
import textwrap
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("pip3 install Pillow")

# Стиль
BG_COLOR   = (8, 8, 8)        # #080808
TEXT_COLOR = (255, 255, 255)   # белый
ACCENT     = (180, 180, 180)   # серый для подзаголовков
W, H       = 1080, 1080        # квадрат для Instagram
PADDING    = 80
LINE_H     = 68
FONT_SIZE  = 52
NUM_SIZE   = 32

OUT_DIR = "/tmp/carousel_slides"


def get_font(size):
    """Ищем лучший доступный шрифт."""
    candidates = [
        "/Library/Fonts/Montserrat-Bold.ttf",
        "/Library/Fonts/Montserrat-Regular.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay-Bold.otf",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/SFNSText.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def make_slide(text, slide_num, total):
    img  = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_main = get_font(FONT_SIZE)
    font_num  = get_font(NUM_SIZE)

    # Номер слайда (правый нижний угол)
    num_text = f"{slide_num}/{total}"
    draw.text((W - PADDING, H - PADDING - NUM_SIZE), num_text,
              font=font_num, fill=ACCENT, anchor="rs")

    # Разбиваем текст на строки
    lines = []
    for paragraph in text.strip().split("\n"):
        wrapped = textwrap.wrap(paragraph, width=22) if paragraph else [""]
        lines.extend(wrapped)

    # Вертикальное центрирование
    total_height = len(lines) * LINE_H
    start_y = (H - total_height) // 2

    for i, line in enumerate(lines):
        y = start_y + i * LINE_H
        # Горизонтальное центрирование
        try:
            bbox = draw.textbbox((0, 0), line, font=font_main)
            text_w = bbox[2] - bbox[0]
        except Exception:
            text_w = len(line) * (FONT_SIZE // 2)
        x = (W - text_w) // 2
        draw.text((x, y), line, font=font_main, fill=TEXT_COLOR)

    return img


def generate_carousel(slides_text, out_dir=OUT_DIR):
    """
    slides_text — строки разделённые '---'
    Возвращает список путей к PNG.
    """
    os.makedirs(out_dir, exist_ok=True)
    # Чистим старые слайды
    for f in Path(out_dir).glob("slide_*.png"):
        f.unlink()

    slides = [s.strip() for s in slides_text.split("---") if s.strip()]
    paths  = []

    for i, slide_text in enumerate(slides, 1):
        img  = make_slide(slide_text, i, len(slides))
        path = os.path.join(out_dir, f"slide_{i:02d}.png")
        img.save(path, "PNG")
        paths.append(path)
        print(f"  Слайд {i}/{len(slides)}: {path}")

    return paths


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else (
        "Идеал убивает старт\n\nТы ждёшь пока всё будет идеально\n---\n"
        "Но идеально\nне бывает\n\nБывает сделано\n---\n"
        "Начни сейчас.\nДоделай потом.\n\n— sviridovss"
    )
    paths = generate_carousel(text)
    print(f"\nГотово: {len(paths)} слайдов в {OUT_DIR}")
