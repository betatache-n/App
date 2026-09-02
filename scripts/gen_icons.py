from PIL import Image, ImageDraw

BG = (75, 107, 96, 255)       # --accent
FG = (246, 244, 239, 255)     # --bg (near-white, used as icon mark color)

def draw_mark(draw, size):
    # Simple gauge/battery glyph echoing the app's battery indicator UI.
    cx, cy = size / 2, size / 2
    body_w, body_h = size * 0.46, size * 0.30
    x0, y0 = cx - body_w / 2, cy - body_h / 2
    x1, y1 = cx + body_w / 2, cy + body_h / 2
    stroke = max(2, round(size * 0.035))
    draw.rounded_rectangle([x0, y0, x1, y1], radius=size * 0.03, outline=FG, width=stroke)
    # terminal nub
    nub_w, nub_h = size * 0.035, body_h * 0.4
    draw.rectangle([x1, cy - nub_h / 2, x1 + nub_w, cy + nub_h / 2], fill=FG)
    # fill level (~70%)
    pad = stroke * 1.8
    fill_w = (body_w - pad * 2) * 0.7
    draw.rectangle([x0 + pad, y0 + pad, x0 + pad + fill_w, y1 - pad], fill=FG)

def make_icon(path, size, maskable=False):
    img = Image.new("RGBA", (size, size), BG)
    draw = ImageDraw.Draw(img)
    if maskable:
        # keep the mark inside the safe zone (~80% of canvas) for adaptive icons
        inset = size * 0.1
        sub = Image.new("RGBA", (round(size - inset * 2), round(size - inset * 2)), (0, 0, 0, 0))
        sub_draw = ImageDraw.Draw(sub)
        draw_mark(sub_draw, sub.size[0])
        img.paste(sub, (round(inset), round(inset)), sub)
    else:
        draw_mark(draw, size)
    img.save(path)

make_icon("/home/user/App/icons/icon-192.png", 192)
make_icon("/home/user/App/icons/icon-512.png", 512)
make_icon("/home/user/App/icons/icon-maskable-512.png", 512, maskable=True)
make_icon("/home/user/App/icons/apple-touch-icon.png", 180)
print("done")
