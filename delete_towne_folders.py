import os
import shutil
import xml.etree.ElementTree as ET

base_dir = "C:/testing"

def should_delete_folder(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        customer_name = root.find(".//customer_name")
        if customer_name is not None and any(name in customer_name.text for name in [
            "Towne Properties",
            "Resort Management and Consulting Group",
            "Sienna Community Management, LLC",
            "Vesta Property Services"
        ]):
            return True
    except Exception as e:
        print(f"Error parsing {xml_path}: {e}")
    return False

def delete_matching_folders():
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        xml_file_path = None

        for file in os.listdir(folder_path):
            if file.lower().endswith(".xml"):
                xml_file_path = os.path.join(folder_path, file)
                break

        if xml_file_path and should_delete_folder(xml_file_path):
            print(f"Deleting folder: {folder_path}")
            try:
                shutil.rmtree(folder_path)
            except Exception as e:
                print(f"Failed to delete {folder_path}: {e}")

if __name__ == "__main__":
    delete_matching_folders()
