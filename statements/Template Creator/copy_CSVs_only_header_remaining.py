import os
import pandas as pd
import logging

# === Config ===
SOURCE_DIR = r"C:\testing\statements"
DEST_DIR = r"C:\testing\statements\Template Creator"
LOG_FILE = os.path.join(DEST_DIR, "log.txt")

# === Setup Logging ===
if not os.path.exists(DEST_DIR):
    os.makedirs(DEST_DIR)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s   %(levelname)-5s %(message)s',
    filemode='w'
)

logging.info("=== Header-Only CSV Copy Start ===")

# === Trackers ===
success_count = 0
error_files = []

# === Scan and Process ===
for root, dirs, files in os.walk(SOURCE_DIR):
    if DEST_DIR in root:
        continue  # Skip the output folder
    for file in files:
        if file.lower().endswith(".csv"):
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, SOURCE_DIR)
            flat_name = rel_path.replace("\\", "_")
            dest_file = os.path.join(DEST_DIR, flat_name)

            try:
                # Read just the header row
                df = pd.read_csv(file_path, nrows=0)
                df.to_csv(dest_file, index=False)
                success_count += 1
                logging.info(f"Copied header from: {file_path}")
            except Exception as e:
                error_files.append(flat_name)
                logging.error(f"Failed to process {file_path}: {e}")

# === Summary Logging ===
logging.info("=== Summary ===")
logging.info(f"Total CSVs processed: {success_count}")
logging.info(f"Total CSVs with errors: {len(error_files)}")
logging.info("=== Header-Only CSV Copy End ===")
