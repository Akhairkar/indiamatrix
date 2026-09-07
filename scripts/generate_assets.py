import os
import zlib
import struct
import math

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_dir = os.path.join(root_dir, 'assets', 'images')
os.makedirs(img_dir, exist_ok=True)

def write_png(filepath, width, height, pixel_func):
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    
    header = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)  # Filter type 0 (None)
        for x in range(width):
            r, g, b = pixel_func(x, y, width, height)
            raw_data.extend([int(r) & 0xff, int(g) & 0xff, int(b) & 0xff])
    idat = chunk(b'IDAT', zlib.compress(bytes(raw_data), 9))
    iend = chunk(b'IEND', b'')
    with open(filepath, 'wb') as f:
        f.write(header + ihdr + idat + iend)

# 1. Generate og-cover.png (1200 x 630)
def og_pixel(x, y, w, h):
    # Base navy gradient
    nx = x / w
    ny = y / h
    base_r = 13 + int(12 * nx)
    base_g = 20 + int(15 * ny)
    base_b = 36 + int(24 * (nx * 0.5 + ny * 0.5))
    
    # Saffron glow at top-right
    dist_tr = math.sqrt((x - w * 0.85)**2 + (y - h * 0.2)**2)
    saff_glow = max(0.0, 1.0 - (dist_tr / 450.0))
    
    # Teal glow at bottom-left
    dist_bl = math.sqrt((x - w * 0.15)**2 + (y - h * 0.8)**2)
    teal_glow = max(0.0, 1.0 - (dist_bl / 450.0))
    
    # Grid lines (every 40px)
    is_grid = (x % 40 == 0) or (y % 40 == 0)
    grid_boost = 12 if is_grid else 0
    
    # Center card border (400, 140 to 800, 490)
    in_center = (250 <= x <= 950 and 150 <= y <= 480)
    border_dist = min(abs(x - 250), abs(x - 950), abs(y - 150), abs(y - 480)) if in_center else 999
    is_border = (border_dist <= 2) and in_center
    
    r = base_r + int(saff_glow * 180 * 0.4) + grid_boost
    g = base_g + int(saff_glow * 120 * 0.3 + teal_glow * 180 * 0.4) + grid_boost
    b = base_b + int(teal_glow * 160 * 0.4) + grid_boost
    
    if in_center:
        r = int(r * 0.85 + 18)
        g = int(g * 0.85 + 28)
        b = int(b * 0.85 + 46)
        
    if is_border:
        r = 45
        g = 212
        b = 191
        
    return (min(255, r), min(255, g), min(255, b))

og_path = os.path.join(img_dir, 'og-cover.png')
write_png(og_path, 1200, 630, og_pixel)
print(f"Generated {og_path} (1200x630)")

# 2. Generate logo.png (512 x 512)
def logo_pixel(x, y, w, h):
    cx, cy = w / 2, h / 2
    d = math.sqrt((x - cx)**2 + (y - cy)**2)
    if d > 240:
        return (13, 20, 36)
    if d > 230:
        return (45, 212, 191) # Teal ring
    if d > 220:
        return (255, 153, 51) # Saffron ring
    # Inner dark disc with gradient
    nx = x / w
    r = int(18 + nx * 20)
    g = int(26 + nx * 30)
    b = int(48 + nx * 40)
    return (r, g, b)

logo_path = os.path.join(img_dir, 'logo.png')
write_png(logo_path, 512, 512, logo_pixel)
print(f"Generated {logo_path} (512x512)")

# 3. Generate favicon-32x32.png
def fav32_pixel(x, y, w, h):
    # Rounded rect
    in_box = (2 <= x <= 29 and 2 <= y <= 29)
    if not in_box:
        return (13, 20, 36)
    if x in (2, 29) or y in (2, 29):
        return (45, 212, 191)
    if 10 <= x <= 21 and 10 <= y <= 21:
        return (255, 153, 51)
    return (18, 28, 48)

fav32_path = os.path.join(img_dir, 'favicon-32x32.png')
write_png(fav32_path, 32, 32, fav32_pixel)
print(f"Generated {fav32_path} (32x32)")

# 4. Generate apple-touch-icon.png (180x180)
def apple_pixel(x, y, w, h):
    cx, cy = w / 2, h / 2
    d = math.sqrt((x - cx)**2 + (y - cy)**2)
    if d > 85:
        return (13, 20, 36)
    if d > 80:
        return (45, 212, 191)
    return (22, 34, 58)

apple_path = os.path.join(img_dir, 'apple-touch-icon.png')
write_png(apple_path, 180, 180, apple_pixel)
print(f"Generated {apple_path} (180x180)")

# 5. Generate favicon.svg
favicon_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#0D1424" stroke="#2DD4BF" stroke-width="3"/>
  <circle cx="20" cy="20" r="6" fill="#FF9933"/>
  <text x="32" y="44" fill="#2DD4BF" font-family="system-ui, -apple-system, sans-serif" font-weight="800" font-size="28" text-anchor="middle">IM</text>
</svg>
'''
with open(os.path.join(img_dir, 'favicon.svg'), 'w', encoding='utf-8') as f:
    f.write(favicon_svg)
print("Generated favicon.svg")
