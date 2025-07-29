import os
import csv
import shutil
from pathlib import Path

# --- CONFIG ---
TRIMMED_DIR = Path(r"C:\testing\statements\Template Creator\Trimmed")
LOG_FILE = TRIMMED_DIR / "log.txt"

def normalize_header(header):
    return [h.strip().lower() for h in header if h and not h.lower().startswith("unnamed")]

def get_first_csv_file():
    for f in sorted(TRIMMED_DIR.glob("*.csv")):
        return f
    return None

def read_csv_headers(file_path):
    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                return normalize_header(row)
    except Exception as e:
        log(f"ERROR reading {file_path.name}: {e}")
    return []

def compare_headers(h1, h2):
    return h1 == h2

def get_next_group_number():
    existing = [f.name for f in TRIMMED_DIR.iterdir() if f.is_dir() and f.name.lower().startswith("group")]
    nums = [int(name.split()[-1]) for name in existing if name.split()[-1].isdigit()]
    return max(nums, default=0) + 1

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

def main():
    log("\n=== Grouping Run Start ===")

    seed_csv = get_first_csv_file()
    if not seed_csv:
        log("No CSV files found in Trimmed.")
        return

    seed_headers = read_csv_headers(seed_csv)
    if not seed_headers:
        log(f"Seed file {seed_csv.name} has no headers or failed to read.")
        return

    group_num = get_next_group_number()
    group_dir = TRIMMED_DIR / f"Group {group_num}"
    group_dir.mkdir(exist_ok=True)

    moved_files = []

    for file in sorted(TRIMMED_DIR.glob("*.csv")):
        headers = read_csv_headers(file)
        if headers and compare_headers(seed_headers, headers):
            try:
                shutil.move(str(file), group_dir / file.name)
                moved_files.append(file.name)
            except Exception as e:
                log(f"ERROR moving {file.name}: {e}")

    if moved_files:
        log(f"Group {group_num} created with {len(moved_files)} file(s):")
        for f in moved_files:
            log(f"  - {f}")
    else:
        log("No matching files found. Group not created.")

    log("=== Grouping Run End ===\n")

if __name__ == "__main__":
    main()
