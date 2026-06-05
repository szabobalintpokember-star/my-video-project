import os
import sys
from PIL import Image
import numpy as np

# ============================================================
# WW2 VIDEO — GRID CUTTER
# Give it the big grid image, it cuts every cell out and
# saves each one named by its video timestamp.
# ============================================================

TIMESTAMPS = [
    "0.00", "0.03", "0.06", "0.09", "0.12", "0.15", "0.18", "0.22",
    "0.25", "0.29", "0.33", "0.37", "0.40", "0.45", "0.49", "0.53",
    "0.57", "1.01", "1.04", "1.08", "1.12", "1.16", "1.21", "1.25",
    "1.28", "1.31", "1.34", "1.37", "1.40", "1.44", "1.48", "1.51",
    "1.55", "1.58", "2.01", "2.04", "2.09", "2.14", "2.17", "2.20",
    "2.23", "2.26", "2.29", "2.32", "2.35", "2.38", "2.41", "2.44",
    "2.47", "2.50", "2.54", "2.57", "3.01", "3.04", "3.10", "3.13",
    "3.16", "3.19", "3.22", "3.25",
]


def find_dividers(pixel_array, axis, threshold=200, min_gap=20):
    """
    Scan along an axis and find lines where the average brightness
    is above threshold — these are the white/light dividing lines
    between grid cells.
    """
    avg = pixel_array.mean(axis=axis)
    dividers = []
    in_divider = False
    start = 0

    for i, val in enumerate(avg):
        if val >= threshold:
            if not in_divider:
                in_divider = True
                start = i
        else:
            if in_divider:
                in_divider = False
                mid = (start + i) // 2
                if not dividers or (mid - dividers[-1]) >= min_gap:
                    dividers.append(mid)

    if in_divider:
        mid = (start + len(avg)) // 2
        dividers.append(mid)

    return dividers


def cut_grid(image_path, output_folder):
    img = Image.open(image_path).convert("RGB")
    pixels = np.array(img)

    print(f"Image size: {img.width} x {img.height}")

    # Find horizontal dividers (rows) — scan columns, average across width
    gray = pixels.mean(axis=2)  # convert to grayscale values
    row_dividers = find_dividers(gray, axis=1, threshold=220, min_gap=30)
    col_dividers = find_dividers(gray, axis=0, threshold=220, min_gap=30)

    # Add image edges as boundaries
    row_bounds = [0] + row_dividers + [img.height]
    col_bounds = [0] + col_dividers + [img.width]

    rows = len(row_bounds) - 1
    cols = len(col_bounds) - 1
    total = rows * cols

    print(f"Detected grid: {rows} rows x {cols} cols = {total} cells")
    print(f"Timestamps available: {len(TIMESTAMPS)}")

    if total == 0:
        print("ERROR: Could not detect grid. Try manual mode (see below).")
        return

    os.makedirs(output_folder, exist_ok=True)

    cell_index = 0
    saved = 0

    for r in range(rows):
        for c in range(cols):
            if cell_index >= len(TIMESTAMPS):
                print(f"Note: more cells than timestamps — stopping at {len(TIMESTAMPS)}")
                break

            top    = row_bounds[r]
            bottom = row_bounds[r + 1]
            left   = col_bounds[c]
            right  = col_bounds[c + 1]

            # Skip tiny slivers (divider artifacts)
            if (bottom - top) < 30 or (right - left) < 30:
                continue

            cell = img.crop((left, top, right, bottom))
            timestamp = TIMESTAMPS[cell_index]
            filename = f"{timestamp}.png"
            out_path = os.path.join(output_folder, filename)
            cell.save(out_path)
            print(f"  Saved: {filename}  ({left},{top}) → ({right},{bottom})")
            cell_index += 1
            saved += 1

    print(f"\nDone! {saved} images saved to: {output_folder}")


def manual_cut(image_path, output_folder, rows, cols):
    """Fallback: divide image into equal rows x cols grid."""
    img = Image.open(image_path).convert("RGB")
    cell_w = img.width // cols
    cell_h = img.height // rows
    total = rows * cols

    print(f"Manual mode: {rows} rows x {cols} cols = {total} cells")
    print(f"Cell size: {cell_w} x {cell_h} px")

    os.makedirs(output_folder, exist_ok=True)

    cell_index = 0
    for r in range(rows):
        for c in range(cols):
            if cell_index >= len(TIMESTAMPS):
                break
            left   = c * cell_w
            top    = r * cell_h
            right  = left + cell_w
            bottom = top + cell_h
            cell = img.crop((left, top, right, bottom))
            timestamp = TIMESTAMPS[cell_index]
            filename = f"{timestamp}.png"
            cell.save(os.path.join(output_folder, filename))
            print(f"  Saved: {filename}")
            cell_index += 1

    print(f"\nDone! {cell_index} images saved to: {output_folder}")


if __name__ == "__main__":
    # --- Get image path ---
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("Paste the full path to your grid image and press Enter:\n> ").strip().strip('"')

    if not os.path.exists(image_path):
        print(f"ERROR: File not found: {image_path}")
        input("Press Enter to close...")
        sys.exit(1)

    # --- Output folder (same folder as image, subfolder 'cut_images') ---
    output_folder = os.path.join(os.path.dirname(os.path.abspath(image_path)), "cut_images")

    print("\nChoose mode:")
    print("  1 = Auto-detect grid (recommended)")
    print("  2 = Manual (you specify rows and columns)")
    mode = input("> ").strip()

    if mode == "2":
        rows = int(input("How many rows in the grid? > ").strip())
        cols = int(input("How many columns in the grid? > ").strip())
        manual_cut(image_path, output_folder, rows, cols)
    else:
        cut_grid(image_path, output_folder)

    print(f"\nImages are in: {output_folder}")
    input("\nPress Enter to close...")
