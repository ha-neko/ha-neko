from PIL import Image, ImageDraw, ImageFilter
import math

W, H = 200, 260
FRAMES = 24
COLORS = {
    "outer": (133, 183, 235),    # 85b7eb blue
    "mid":   (93, 202, 165),     # 5DCAA5 green
    "inner": (237, 147, 177),    # ed93b1 pink
    "core":  (158, 225, 203),    # 9FE1CB light green
}

def flame_outline(t, time):
    base_w = 55 * (1 - t) + 18 * (1 - t) ** 2
    wave = math.sin(t * 10 + time * 0.5) * 5 * (1 - t)
    split = abs(math.sin(time * 0.15)) * 8 * t ** 4
    flicker = math.sin(time * 0.3 + t * 3) * 4 * (1 - t)
    bw = base_w + wave + flicker
    return bw

frames = []
for f in range(FRAMES):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, by = W // 2, H - 25

    layers = [
        (COLORS["outer"], 1.0, 20),
        (COLORS["mid"],   0.7, 14),
        (COLORS["inner"], 0.4, 8),
        (COLORS["core"],  0.15, 3),
    ]

    for color, scale, thickness in layers:
        pts = []
        for i in range(80):
            t = i / 80
            bw = flame_outline(t, f) * scale
            x = cx + bw * math.cos(t * 1.8)
            y = by - t * (H - 50)
            pts.append((x, y))
        for i in range(len(pts) - 1):
            tw = max(1, int(thickness * (0.3 + 0.7 * (1 - i / len(pts)))))
            draw.line([pts[i], pts[i + 1]], fill=color, width=tw)

    glow = img.filter(ImageFilter.GaussianBlur(radius=6))
    img = Image.alpha_composite(glow, img)
    frames.append(img.convert("P", palette=Image.ADAPTIVE, colors=32))

frames[0].save("flame.gif", save_all=True, append_images=frames[1:],
                optimize=False, duration=100, loop=0, disposal=2)
print("OK: flame.gif")
