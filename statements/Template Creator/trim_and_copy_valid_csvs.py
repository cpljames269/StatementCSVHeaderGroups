import os
import pandas as pd
import logging
import difflib

# === Config ===
SOURCE_DIR = r"C:\testing\statements\Template Creator"
DEST_DIR = os.path.join(SOURCE_DIR, "Trimmed")
LOG_FILE = os.path.join(SOURCE_DIR, "log.txt")
FUZZY_TARGET = "Beginning Balance Amount"

# === Setup Logging ===
if not os.path.exists(DEST_DIR):
    os.makedirs(DEST_DIR)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s   %(levelname)-5s %(message)s",
    filemode="w"
)

logging.info("=== Trim Script Start ===")

# === Helper: Normalize header ===
def norm_header(h):
    return ''.join(c.lower() for c in h if c.isalnum())

# === Main Processing ===
processed = 0
skipped = 0
errors = 0

for file in os.listdir(SOURCE_DIR):
    file_path = os.path.join(SOURCE_DIR, file)
    if not file.lower().endswith(".csv") or not os.path.isfile(file_path):
        continue

    try:
        # Try various encodings for robustness
        try:
            df = pd.read_csv(file_path, dtype=str)
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='utf-8-sig', dtype=str)
        except Exception:
            df = pd.read_csv(file_path, encoding='latin1', dtype=str)

        # Drop unnamed/blank headers
        original_columns = df.columns.tolist()
        clean_columns = [col for col in original_columns if col.strip() and not col.strip().lower().startswith("unnamed")]
        df = df[clean_columns]

        dropped = [col for col in original_columns if col not in clean_columns]
        if dropped:
            logging.info(f"Dropped invalid headers in: {file} — {dropped}")

        # Normalize and find fuzzy match
        normalized = [norm_header(c) for c in df.columns]
        match_index = None
        for i, col in enumerate(normalized):
            ratio = difflib.SequenceMatcher(None, col, norm_header(FUZZY_TARGET)).ratio()
            if ratio >= 0.75:
                match_index = i
                break

        if match_index is None:
            logging.warning(f"Skipped: No fuzzy match for '{FUZZY_TARGET}' in {file}")
            skipped += 1
            continue

        # Trim columns after the match index
        trimmed_df = df.iloc[:, :match_index + 1]
        if trimmed_df.shape[1] == 0:
            logging.warning(f"Skipped: Trimmed result has no columns in {file}")
            skipped += 1
            continue

        # Clean filename and write
        filename = file.replace("original", "").rstrip("_").rstrip("-").strip()
        trimmed_file_path = os.path.join(DEST_DIR, filename)
        trimmed_df.to_csv(trimmed_file_path, index=False)
        logging.info(f"Trimmed and saved: {filename}")
        processed += 1

    except Exception as e:
        logging.error(f"Error processing {file}: {e}")
        errors += 1

# === Summary ===
logging.info("=== Trim Script Summary ===")
logging.info(f"Total processed: {processed}")
logging.info(f"Total skipped: {skipped}")
logging.info(f"Total errors: {errors}")
logging.info("=== Trim Script End ===")
