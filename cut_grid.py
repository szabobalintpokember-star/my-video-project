from PIL import Image
import numpy as np
import os
import sys

print("=" * 50)
print("  WW2 VIDEO — IMAGE CUTTER")
print("  Cuts your big grid picture into")
print("  60 separate images, named by timestamp")
print("=" * 50)
print()

# ── STEP 1: Ask for the image ────────────────────────
print("STEP 1 of 3 — Find your grid image")
print()
print("  How to get the path:")
print("  → Right-click your image file")
print("  → Click 'Copy as path'")
print("  → Paste it below")
print()
image_path = input("  Paste image path here: ").strip().strip('"').strip("'")
print()

if not os.path.exists(image_path):
    print("  ERROR: Can't find that file.")
    print(f"  You typed: {image_path}")
    print("  Make sure you copied the path correctly.")
    input("\n  Press Enter to close...")
    sys.exit()

print("  ✓ Image found!")
print()

# ── STEP 2: Ask for grid size ────────────────────────
print("STEP 2 of 3 — Tell me the grid size")
print()
print("  Look at your grid image and count:")
print("  → How many images across? (columns)")
print("  → How many images down?   (rows)")
print()
print("  Example: if it's 10 wide and 6 tall, type 10 then 6")
print()

while True:
    try:
        cols = int(input("  How many columns (images across)? "))
        rows = int(input("  How many rows    (images down)?   "))
        break
    except ValueError:
        print("  Please type a number only (like 10 or 6)")

print()

# ── STEP 3: Cut and save ─────────────────────────────
print("STEP 3 of 3 — Cutting and saving images...")
print()

TIMESTAMPS = [
    "0.00", "0.03", "0.06", "0.09", "0.12", "0.15", "0.18", "0.22",
    "0.25", "0.29", "0.33", "0.37", "0.40", "0.45", "0.49", "0.53",
    "0.57", "1.01", "1.04", "1.08", "1.12", "1.16", "1.21", "1.25",
    "1.28", "1.31", "1.34", "1.37", "1.40", "1.44", "1.48", "1.51",
    "1.55", "1.58", "2.01", "2.04", "2.09", "2.14", "2.17", "2.20",
    "2.23", "2.26", "2.29", "2.32", "2.35", "2.38", "2.41", "2.44",
    "2.47", "2.50", "2.54", "2.57", "3.01", "3.04", "3.10", "3.13",
    "3.16", "3.19", "3.22", "3.25", "3.29", "3.32", "3.35", "3.38",
    "3.43", "3.47", "3.51", "3.54", "3.57", "4.02", "4.06", "4.10",
    "4.13", "4.16", "4.20", "4.23", "4.26", "4.29", "4.33", "4.37",
    "4.41", "4.44", "4.47", "4.50", "4.53", "4.57", "5.00", "5.03",
]

img        = Image.open(image_path).convert("RGB")
cell_w     = img.width  // cols
cell_h     = img.height // rows
total_cells = rows * cols

# Save into a new folder next to the original image
image_dir     = os.path.dirname(os.path.abspath(image_path))
output_folder = os.path.join(image_dir, "WW2_Cut_Images")
os.makedirs(output_folder, exist_ok=True)

saved  = 0
skipped = 0

for r in range(rows):
    for c in range(cols):
        index = r * cols + c

        if index >= len(TIMESTAMPS):
            skipped += 1
            continue

        left   = c * cell_w
        top    = r * cell_h
        right  = left + cell_w
        bottom = top  + cell_h

        cell      = img.crop((left, top, right, bottom))
        filename  = f"{TIMESTAMPS[index]}.png"
        save_path = os.path.join(output_folder, filename)
        cell.save(save_path)

        saved += 1
        print(f"  Saved {saved:>2}/{min(total_cells, len(TIMESTAMPS))}  →  {filename}")

# ── Done ─────────────────────────────────────────────
print()
print("=" * 50)
print(f"  DONE!  {saved} images saved.")
print()
print(f"  Your images are here:")
print(f"  {output_folder}")
print()
print("  Next step:")
print("  → Open CapCut")
print("  → Import all images from that folder")
print("  → Sort by name — they will be in perfect order")
print("=" * 50)

input("\n  Press Enter to close...")
