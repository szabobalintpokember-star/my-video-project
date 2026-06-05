import os
import sys

# ============================================================
# WW2 VIDEO — AUTO IMAGE RENAMER
# Drop all your ChatGPT images into a folder, run this script,
# and every image gets renamed to match its video timestamp.
# ============================================================

TIMESTAMP_NAMES = [
    "0.00",
    "0.03",
    "0.06",
    "0.09",
    "0.12",
    "0.15",
    "0.18",
    "0.22",
    "0.25",
    "0.29",
    "0.33",
    "0.37",
    "0.40",
    "0.45",
    "0.49",
    "0.53",
    "0.57",
    "1.01",
    "1.04",
    "1.08",
    "1.12",
    "1.16",
    "1.21",
    "1.25",
    "1.28",
    "1.31",
    "1.34",
    "1.37",
    "1.40",
    "1.44",
    "1.48",
    "1.51",
    "1.55",
    "1.58",
    "2.01",
    "2.04",
    "2.09",
    "2.14",
    "2.17",
    "2.20",
    "2.23",
    "2.26",
    "2.29",
    "2.32",
    "2.35",
    "2.38",
    "2.41",
    "2.44",
    "2.47",
    "2.50",
    "2.54",
    "2.57",
    "3.01",
    "3.04",
    "3.10",
    "3.13",
    "3.16",
    "3.19",
    "3.22",
    "3.25",
    "3.29",
    "3.32",
    "3.35",
    "3.38",
    "3.43",
    "3.47",
    "3.51",
    "3.54",
    "3.57",
    "4.02",
    "4.06",
    "4.10",
    "4.13",
    "4.16",
    "4.20",
    "4.23",
    "4.26",
    "4.29",
    "4.33",
    "4.37",
    "4.41",
    "4.44",
    "4.47",
    "4.50",
    "4.53",
    "4.57",
    "5.00",
    "5.03",
]

def rename_images(folder_path):
    if not os.path.exists(folder_path):
        print(f"ERROR: Folder not found: {folder_path}")
        return

    # Get all image files sorted by name (assumes ChatGPT saves them in order)
    extensions = (".png", ".jpg", ".jpeg", ".webp")
    files = sorted([
        f for f in os.listdir(folder_path)
        if f.lower().endswith(extensions)
    ])

    if not files:
        print("ERROR: No image files found in that folder.")
        return

    print(f"Found {len(files)} images. Renaming...\n")

    total = min(len(files), len(TIMESTAMP_NAMES))

    for i in range(total):
        old_name = files[i]
        ext = os.path.splitext(old_name)[1].lower()
        new_name = f"{TIMESTAMP_NAMES[i]}{ext}"
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"  {old_name}  →  {new_name}")

    print(f"\nDone! {total} images renamed.")

    if len(files) > len(TIMESTAMP_NAMES):
        print(f"WARNING: You had {len(files)} images but only {len(TIMESTAMP_NAMES)} timestamps defined.")
    elif len(files) < len(TIMESTAMP_NAMES):
        print(f"NOTE: Only {len(files)} images found — {len(TIMESTAMP_NAMES) - len(files)} timestamps have no image yet.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = input("Paste the path to your images folder and press Enter:\n> ").strip().strip('"')

    rename_images(folder)
    input("\nPress Enter to close...")
