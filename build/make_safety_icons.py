#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从中文安全图生成英文版安全图。

中文那四张（LITEARM_SE_images/safety/*.png）是「三角形图示 + 一行中文」拼在
一起的位图，图示部分与语言无关，中文只在下半部分。本脚本按横贯整幅图的那条
空白间隙把图示和中文裁开，保留图示原样，在下方用 Lato Black 重排英文标签，
写到 LITEARM_SE_images/safety/en/。

英文标签用的是行业惯用的写法，与 iso 7010 的图示名一致：
    danger.png    -> DANGER
    warning.png   -> WARNING
    high_temp.png -> HIGH TEMPERATURE（两行，高窄的图放不下单行）
    notice.png    -> NOTICE

中文图不改动。重跑本脚本会覆盖 en/ 下的产物，所以不要手改那些 PNG。

用法：python3 build/make_safety_icons.py
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "LITEARM_SE_images", "safety")
DST = os.path.join(SRC, "en")

# 正文字体是 Lato，标签沿用它，和手册排版一致。
FONT_PATH = "/usr/share/fonts/truetype/lato/Lato-Black.ttf"
FONT_SIZE = 24
LINE_SPACING = 1.15
# 图文之间的留白，取中文原图里那条间隙的视觉效果
GAP = 12
PAD = 6

LABELS = {
    "danger.png": ["DANGER"],
    "warning.png": ["WARNING"],
    "high_temp.png": ["HIGH", "TEMPERATURE"],
    "notice.png": ["NOTICE"],
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def ink_mask(img):
    """1 位掩膜：非白像素为 1，getbbox() 即内容范围。"""
    return img.convert("L").point(lambda v: 255 if v < 240 else 0, mode="1")


def split_pictogram(img):
    """按图示与标签之间的空白间隙切开，返回图示部分的裁剪结果。"""
    img = img.convert("RGB")
    mask = ink_mask(img)
    top = mask.getbbox()[1]
    row = top
    while row < img.height and mask.crop((0, row, img.width, row + 1)).getbbox():
        row += 1                       # 一直走到图示结束
    if row >= img.height:
        raise SystemExit("no blank gap between pictogram and label")

    band = img.crop((0, top, img.width, row))
    return band.crop(ink_mask(band).getbbox())


def render(src_name, lines, font):
    pict = split_pictogram(Image.open(os.path.join(SRC, src_name)))
    line_w = [font.getlength(t) for t in lines]
    line_h = int(round(FONT_SIZE * LINE_SPACING))

    width = max(pict.width, int(max(line_w))) + 2 * PAD
    height = pict.height + GAP + line_h * len(lines)

    out = Image.new("RGB", (width, height), WHITE)
    out.paste(pict, ((width - pict.width) // 2, 0))

    draw = ImageDraw.Draw(out)
    y = pict.height + GAP
    for text in lines:
        draw.text((width // 2, y), text, font=font, fill=BLACK, anchor="mt")
        y += line_h
    return out


def main():
    if not os.path.isfile(FONT_PATH):
        print("font not found: %s" % FONT_PATH, file=sys.stderr)
        return 1
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    os.makedirs(DST, exist_ok=True)

    for name, lines in LABELS.items():
        out = render(name, lines, font)
        path = os.path.join(DST, name)
        out.save(path)
        print("%s -> %s  %dx%d  %s" % (name, os.path.relpath(path, ROOT), out.width, out.height, " / ".join(lines)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
