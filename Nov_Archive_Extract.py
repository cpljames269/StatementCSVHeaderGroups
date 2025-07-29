import os
import shutil
import logging
import time

# Set source and destination base directories
source_base = r"\\192.168.2.2\Design\HOA Admin\hoa_v2\02_archive\2024"
destination_base = r"C:\testing"

# Set up logging
log_file = os.path.join(destination_base, "logs", "Dec_Archive_Extract.log")
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Start timer
start_time = time.time()
logging.info("Script started.")

# Process October only
target_months = ["12_December"]

for month_folder in target_months:
    month_path = os.path.join(source_base, month_folder)
    if not os.path.isdir(month_path):
        logging.warning(f"Skipping {month_folder}: Not a directory.")
        continue

    for folder_name in os.listdir(month_path):
        folder_path = os.path.join(month_path, folder_name)
        if not os.path.isdir(folder_path):
            continue

        xml_file = None
        csv_file = None

        for file in os.listdir(folder_path):
            if file.endswith("jobticket.xml"):
                xml_file = file
            elif file.endswith("original.csv"):
                csv_file = file

        if not xml_file or not csv_file:
            logging.warning(f"Skipping {folder_name} in {month_folder}: Missing required file(s).")
            continue

        dest_dir = os.path.join(destination_base, folder_name)
        os.makedirs(dest_dir, exist_ok=True)

        try:
            shutil.copy2(os.path.join(folder_path, xml_file), os.path.join(dest_dir, xml_file))
            shutil.copy2(os.path.join(folder_path, csv_file), os.path.join(dest_dir, csv_file))
            logging.info(f"Copied files for {folder_name} from {month_folder}")
        except Exception as e:
            logging.error(f"Error copying files for {folder_name} from {month_folder}: {str(e)}")

# End timer
end_time = time.time()
elapsed = end_time - start_time
logging.info(f"Script completed in {elapsed:.2f} seconds.")
