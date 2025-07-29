import os
import shutil
import xml.etree.ElementTree as ET

base_dir = "C:/testing"
dest_dir = os.path.join(base_dir, "statements")

os.makedirs(dest_dir, exist_ok=True)

def should_move_folder(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        product_elem = root.find(".//general/product")
        if product_elem is not None and "Statements from CSV" in product_elem.text:
            return True
    except Exception as e:
        print(f"Error parsing {xml_path}: {e}")
    return False

def move_matching_folders():
    folder_count = 0
    moved_count = 0

    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        folder_count += 1
        print(f"Checking folder {folder_count}: {folder_name}")

        xml_file_path = None
        for file in os.listdir(folder_path):
            if file.lower().endswith(".xml"):
                xml_file_path = os.path.join(folder_path, file)
                break

        if xml_file_path and should_move_folder(xml_file_path):
            dest_path = os.path.join(dest_dir, folder_name)
            print(f"Moving: {folder_path} --> {dest_path}")
            try:
                shutil.move(folder_path, dest_path)
                moved_count += 1
            except Exception as e:
                print(f"Failed to move {folder_path}: {e}")

    print(f"Checked {folder_count} folders, moved {moved_count} folders.")

if __name__ == "__main__":
    move_matching_folders()
