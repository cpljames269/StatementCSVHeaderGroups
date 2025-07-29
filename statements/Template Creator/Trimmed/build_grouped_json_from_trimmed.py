import os
import csv
import json
import xml.etree.ElementTree as ET
import unicodedata
from collections import defaultdict

BASE_DIR = r"C:\testing\statements"
TRIMMED_DIR = r"C:\testing\statements\Template Creator\Trimmed"
OUTPUT_JSON = "csv_header_groups.json"

def normalize(text):
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = text.replace('\u00A0', ' ')
    return text.strip().strip('"').strip("'").strip().lower()

def extract_hoa_and_customer(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        customer_name = root.find(".//customer/customer_name").text.strip()
        hoa_name = root.find(".//customer/hoa_name").text.strip()
        return customer_name, hoa_name
    except Exception as e:
        print(f"Error reading XML: {xml_path} - {e}")
        return None, None

def extract_original_header(csv_path):
    try:
        with open(csv_path, newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            headers = next(reader)
            return headers
    except Exception as e:
        print(f"Error reading CSV: {csv_path} - {e}")
        return []

def build_groups_from_trimmed():
    output_data = []

    for group_folder in sorted(os.listdir(TRIMMED_DIR)):
        group_path = os.path.join(TRIMMED_DIR, group_folder)
        if not os.path.isdir(group_path):
            continue

        group_entries = []

        for filename in os.listdir(group_path):
            if not filename.lower().endswith(".csv"):
                continue

            if "_" not in filename:
                print(f"Skipping unexpected filename format: {filename}")
                continue
            part1, part2_with_ext = filename.split("_", 1)
            part2 = part2_with_ext.rsplit(".", 1)[0]

            original_folder = os.path.join(BASE_DIR, part1)
            if not os.path.isdir(original_folder):
                print(f"Original folder not found: {original_folder}")
                continue

            xml_file = None
            for f in os.listdir(original_folder):
                if f.lower().endswith(".xml"):
                    xml_file = os.path.join(original_folder, f)
                    break
            if not xml_file:
                print(f"XML file not found in {original_folder}")
                continue

            csv_file = None
            for f in os.listdir(original_folder):
                if f.lower().endswith(".csv") and part2 in f:
                    csv_file = os.path.join(original_folder, f)
                    break
            if not csv_file:
                print(f"CSV file matching '{part2}' not found in {original_folder}")
                continue

            customer_name, hoa_name = extract_hoa_and_customer(xml_file)
            if not customer_name or not hoa_name:
                continue

            original_header = extract_original_header(csv_file)
            if not original_header:
                continue

            group_entries.append({
                "customer_name": customer_name,
                "hoa_name": hoa_name,
                "folder": part1,
                "original_header": original_header,
                "trimmed_filename": filename
            })

        if group_entries:
            # Group entries by normalized header
            subgroup_map = defaultdict(list)
            for entry in group_entries:
                norm_key = tuple(normalize(h) for h in entry["original_header"])
                subgroup_map[norm_key].append(entry)

            subgroups = []
            for _, entries in subgroup_map.items():
                subgroups.append({
                    "header": entries[0]["original_header"],
                    "matches": entries
                })

            output_data.append({
                "label": group_folder,
                "subgroups": subgroups
            })

    return output_data

def save_to_json(output_data):
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
    print(f"\nSaved grouped result to {OUTPUT_JSON}")

if __name__ == "__main__":
    groups = build_groups_from_trimmed()
    save_to_json(groups)
