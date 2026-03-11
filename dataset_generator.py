from icrawler.builtin import BingImageCrawler
import os

# ── FRESH FRUITS ──────────────────────────────────────────────
fresh_fruits = [
    "fresh apple fruit",
    "fresh banana fruit",
    "fresh orange fruit",
    "fresh mango fruit",
    "fresh grape fruit",
    "fresh pineapple fruit",
    "fresh strawberry fruit",
    "fresh watermelon fruit",
    "fresh papaya fruit",
    "fresh pomegranate fruit"
]

fresh_folder_names = [
    "apple_fruit",
    "banana_fruit",
    "orange_fruit",
    "mango_fruit",
    "grape_fruit",
    "pineapple_fruit",
    "strawberry_fruit",
    "watermelon_fruit",
    "papaya_fruit",
    "pomegranate_fruit"
]

# ── ROTTEN FRUITS ─────────────────────────────────────────────
rotten_fruits = [
    "rotten apple fruit moldy spoiled",
    "rotten banana fruit brown spoiled",
    "rotten orange fruit moldy spoiled",
    "rotten mango fruit spoiled decayed",
    "rotten grape fruit moldy spoiled",
    "rotten pineapple fruit spoiled decayed",
    "rotten strawberry fruit moldy spoiled",
    "rotten watermelon fruit spoiled decayed",
    "rotten papaya fruit spoiled decayed",
    "rotten pomegranate fruit spoiled moldy"
]

rotten_folder_names = [
    "rotten_apple_fruit",
    "rotten_banana_fruit",
    "rotten_orange_fruit",
    "rotten_mango_fruit",
    "rotten_grape_fruit",
    "rotten_pineapple_fruit",
    "rotten_strawberry_fruit",
    "rotten_watermelon_fruit",
    "rotten_papaya_fruit",
    "rotten_pomegranate_fruit"
]

# ── NON FRUIT OBJECTS ─────────────────────────────────────────
nonfruits = [
    "car vehicle road",
    "laptop computer screen",
    "chair furniture indoor",
    "dog animal pet",
    "cat animal pet",
    "plastic bottle water",
    "mobile phone smartphone",
    "wooden table furniture",
    "bus vehicle transport",
    "building architecture outdoor"
]

nonfruit_folder_names = [
    "nonfruit_car",
    "nonfruit_laptop",
    "nonfruit_chair",
    "nonfruit_dog",
    "nonfruit_cat",
    "nonfruit_bottle",
    "nonfruit_mobile_phone",
    "nonfruit_table",
    "nonfruit_bus",
    "nonfruit_building"
]

# ── IMAGE COUNTS ──────────────────────────────────────────────
TRAIN_FRESH    = 200
TRAIN_ROTTEN   = 200
TRAIN_NONFRUIT = 150

TEST_FRESH     = 50
TEST_ROTTEN    = 50
TEST_NONFRUIT  = 40

# ── DOWNLOAD HELPER ───────────────────────────────────────────
def download(keyword, folder, count):
    os.makedirs(folder, exist_ok=True)
    existing = len([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))])
    if existing >= count:
        print(f"  ⏭  Skipping — {folder} already has {existing} images")
        return
    needed = count - existing
    print(f"  ⬇  Downloading {needed} images → {folder}")
    try:
        crawler = BingImageCrawler(
            feeder_threads=2,
            parser_threads=2,
            downloader_threads=4,
            storage={'root_dir': folder}
        )
        crawler.crawl(keyword=keyword, max_num=count, min_size=(80, 80))
    except Exception as e:
        print(f"  ⚠  Error downloading {keyword}: {e}")

# ══════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("   DOWNLOADING TRAIN DATASET")
print("="*60)

print("\n>>> FRESH FRUITS (200 images each)")
for kw, fn in zip(fresh_fruits, fresh_folder_names):
    download(kw, f"dataset/train/{fn}", TRAIN_FRESH)

print("\n>>> ROTTEN FRUITS (200 images each)")
for kw, fn in zip(rotten_fruits, rotten_folder_names):
    download(kw, f"dataset/train/{fn}", TRAIN_ROTTEN)

print("\n>>> NON-FRUIT OBJECTS (150 images each)")
for kw, fn in zip(nonfruits, nonfruit_folder_names):
    download(kw, f"dataset/train/{fn}", TRAIN_NONFRUIT)

# ══════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("   DOWNLOADING TEST DATASET")
print("="*60)

print("\n>>> FRESH FRUITS (50 images each)")
for kw, fn in zip(fresh_fruits, fresh_folder_names):
    download(kw, f"dataset/test/{fn}", TEST_FRESH)

print("\n>>> ROTTEN FRUITS (50 images each)")
for kw, fn in zip(rotten_fruits, rotten_folder_names):
    download(kw, f"dataset/test/{fn}", TEST_ROTTEN)

print("\n>>> NON-FRUIT OBJECTS (40 images each)")
for kw, fn in zip(nonfruits, nonfruit_folder_names):
    download(kw, f"dataset/test/{fn}", TEST_NONFRUIT)

# ══════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("   DATASET SUMMARY")
print("="*60)

total_train = 0
total_test  = 0

for split in ["train", "test"]:
    print(f"\n  {split.upper()}:")
    if not os.path.exists(f"dataset/{split}"):
        continue
    for cls in sorted(os.listdir(f"dataset/{split}")):
        path = f"dataset/{split}/{cls}"
        if not os.path.isdir(path):
            continue
        count = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
        tag = "🍎 FRESH" if not cls.startswith("rotten") and not cls.startswith("nonfruit") else ("🔴 ROTTEN" if cls.startswith("rotten") else "🔵 NONFRUIT")
        print(f"    {tag}  {cls:<35} {count} images")
        if split == "train":
            total_train += count
        else:
            total_test  += count

print(f"\n  Total TRAIN images : {total_train}")
print(f"  Total TEST  images : {total_test}")
print(f"  Total classes      : {len(fresh_fruits) + len(rotten_fruits) + len(nonfruits)} (10 fresh + 10 rotten + 10 nonfruit)")
print("\n✅ Dataset Download Completed!")
print("   Now run: python train_model.py")
