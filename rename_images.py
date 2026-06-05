import os
import sys

# ============================================================
# WW2 VIDEO — AUTO IMAGE RENAMER
# Drop all your ChatGPT images into a folder, run this script,
# and every image gets renamed to match its video timestamp.
# ============================================================

TIMESTAMP_NAMES = [
    "0-00_most-people-think-they-know-ww2",
    "0-03_textbook-and-tv",
    "0-06_the-real-story-question",
    "0-09_dark-clouds-scared-stickman",
    "0-12_nobody-talks-about-this",
    "0-15_five-facts-boxes",
    "0-18_lets-go-running",
    "0-22_fact-1-number",
    "0-25_map-stalingrad",
    "0-29_broken-buildings-6-months",
    "0-33_2-million-casualties",
    "0-37_soviet-vs-american-flag",
    "0-40_400k-american-dead",
    "0-45_world-map-all-fronts",
    "0-49_stalingrad-mouth-eating",
    "0-53_street-by-street",
    "0-57_building-floor-by-floor",
    "1-01_room-by-room",
    "1-04_sniper-hiding-in-rubble",
    "1-08_less-than-24-hours",
    "1-12_soviet-flag-planted",
    "1-16_history-book-crossed-out",
    "1-21_fact-2-number-shocked",
    "1-25_german-soldier-gift-box",
    "1-28_tank-bomb-crossed-out-pill",
    "1-31_methamphetamine-pill",
    "1-34_pervitin-chocolate-bar",
    "1-37_handing-out-pills",
    "1-40_blitzkrieg-map-arrow",
    "1-44_spiral-eyes-no-sleep",
    "1-48_cant-stop-sign",
    "1-51_factory-35-million-pills",
    "1-55_high-crash-arc",
    "1-58_addiction-soldiers",
    "2-01_lost-his-mind",
    "2-04_third-reich-eagle-pills",
    "2-09_fact-3-most-unbelievable",
    "2-14_hiroo-onoda-portrait",
    "2-17_map-philippines-jungle",
    "2-20_japan-surrenders-1945",
    "2-23_nobody-told-him-jungle",
    "2-26_fake-news-skeptical",
    "2-29_still-fighting-1945",
    "2-32_timeline-1945-to-1974",
    "2-35_dense-jungle-hiding",
    "2-38_crouching-behind-bush",
    "2-41_leaflet-kicked-away",
    "2-44_family-ignored",
    "2-47_1974-calendar",
    "2-50_airplane-landing-jungle",
    "2-54_stand-down-order",
    "2-57_rifle-placed-on-ground",
    "3-01_age-52-soldier",
    "3-04_war-over-before-born",
    "3-10_fact-4-number-shocked",
    "3-13_map-europe-may-1945",
    "3-16_american-german-same-direction",
    "3-19_proposal-at-table",
    "3-22_ceasefire-white-flag",
    "3-25_walking-side-by-side-east",
    "3-29_soviet-arrow-eastern-europe",
    "3-32_eisenhower-says-no",
    "3-35_considering-the-idea",
    "3-38_already-fought-together",
    "3-43_castle-itter-may-5",
    "3-47_protecting-french-prisoners",
    "3-51_ss-attacking-castle",
    "3-54_days-before-surrender-calendar",
    "3-57_cold-war-map-1945",
    "4-02_fact-5-nobody-talks-about",
    "4-06_85-million-dead",
    "4-10_but-wait-blackboard",
    "4-13_not-bullets-red-x",
    "4-16_four-causes-boxes",
    "4-20_map-bengal-1943",
    "4-23_british-crown-india-arrow",
    "4-26_3-million-dead",
    "4-29_siege-of-leningrad-872-days",
    "4-33_eating-wallpaper-shoe-cat",
    "4-37_star-of-david-6-million",
    "4-41_battlefield-crossed-out",
    "4-44_factory-skull-systematic",
    "4-47_globe-cracking",
    "4-50_city-crumbling-family",
    "4-53_never-fired-a-shot",
    "4-57_not-history-lessons",
    "5-00_warnings",
    "5-03_black-screen-remember",
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
        new_name = f"{str(i+1).zfill(2)}_{TIMESTAMP_NAMES[i]}{ext}"
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
