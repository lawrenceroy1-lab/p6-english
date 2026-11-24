"""Save one Canva export as a site picture.
Usage: .venv/bin/python -I tools/save_picture.py <name> <unitNN> '<canva export url>'
Downloads the JPG, trims white space, max 800 px, progressive JPG <= 80 KB,
saves to img/<unitNN>/<name>.jpg. Skips if the file already exists."""
import sys, os, io, urllib.request
from PIL import Image, ImageChops
name, unit, url = sys.argv[1], sys.argv[2], sys.argv[3]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dst = os.path.join(root, "img", unit, name + ".jpg")
if os.path.exists(dst):
    print("exists, skip", dst); sys.exit(0)
os.makedirs(os.path.dirname(dst), exist_ok=True)
data = urllib.request.urlopen(url, timeout=60).read()
im = Image.open(io.BytesIO(data)).convert("RGB")
bg = Image.new("RGB", im.size, (255, 255, 255))
box = ImageChops.difference(im, bg).convert("L").point(lambda p: 255 if p > 18 else 0).getbbox()
if box:
    l, t, r, b = box; pad = 24
    im = im.crop((max(0, l-pad), max(0, t-pad), min(im.width, r+pad), min(im.height, b+pad)))
im.thumbnail((800, 800), Image.LANCZOS)
q = 80
while True:
    im.save(dst, "JPEG", quality=q, progressive=True, optimize=True)
    kb = os.path.getsize(dst) / 1024
    if kb <= 80 or q <= 55: break
    q -= 5
print(f"saved {dst} {im.size} {kb:.0f}KB")
