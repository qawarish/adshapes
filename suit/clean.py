# Removes the seated figure from the neck opening and recolors to the Qawarish palette.
import numpy as np
from PIL import Image
L = np.asarray(Image.open('../images/3.webp').convert('L')).astype(float)
H, W = L.shape
NAVY_L = np.median(L[1250:1350, 50:150]); BG_L = np.median(L[20:200, 20:200])
def first_dark(x, lo=780, hi=955):
    c = L[lo:hi, x]; return lo + int(np.argmax(c < 110))
def last_dark(x, lo=780, hi=955):
    c = L[lo:hi, x]; return lo + len(c) - 1 - int(np.argmax(c[::-1] < 110))
# rim visible on both sides of the figure; fit a quadratic and interpolate across the gap
xs = list(range(430, 476)) + list(range(632, 700))
p = np.polyfit(xs, [first_dark(x) for x in xs], 2)
out = L.copy()
for x in range(464, 671):
    t = np.polyval(p, x) - 0.5
    for y in range(700, last_dark(x)):
        cov = min(max(y + 1 - t, 0.0), 1.0)
        out[y, x] = BG_L + (NAVY_L - BG_L) * cov
navy = np.array([0x10, 0x3b, 0x5e], float); grey = np.array([0xe0] * 3, float); white = np.array([255.] * 3)
t1 = np.clip((out - NAVY_L) / (BG_L - NAVY_L), 0, 1)[..., None]
t2 = np.clip((out - BG_L) / (255 - BG_L), 0, 1)[..., None]
rgb = navy + (grey - navy) * t1
rgb = rgb + (white - rgb) * t2
img = Image.fromarray(rgb.round().astype(np.uint8))
img.save('/home/user/adshapes/suit/suit-glasses.png')
img.resize((W * 2, H * 2), Image.LANCZOS).save('/home/user/adshapes/suit/suit-glasses@2x.png')
img.crop((380, 730, 760, 980)).resize((760, 500), Image.NEAREST).save('crop2.png')
