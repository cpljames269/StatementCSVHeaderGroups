import os
import json

# === Paths ===
BASE_DIR = r"C:\testing\statements"
JSON_PATH = os.path.join(BASE_DIR, "Template Creator", "Trimmed", "csv_header_groups.json")

def enrich_matches(data):
    for group in data:
        for subgroup in group.get("subgroups", []):
            for match in subgroup.get("matches", []):
                filename = match.get("trimmed_filename") or ""
                if "_" not in filename or not filename.lower().endswith(".csv"):
                    print(f"Skipping malformed or missing filename: {filename}")
                    continue

                # Extract folder and file stem
                folder, file_stem = filename.rsplit(".", 1)[0].split("_", 1)
                folder_path = os.path.join(BASE_DIR, folder)

                if not os.path.isdir(folder_path):
                    print(f"❌ Folder not found: {folder_path}")
                    continue

                # Look for XML
                xml_path = ""
                for f in os.listdir(folder_path):
                    if f.lower().endswith("-jobticket.xml"):
                        xml_path = os.path.join(folder_path, f)
                        break
                if not xml_path:
                    print(f"❌ No jobticket.xml in {folder_path}")

                # Look for CSV like 102724146original.csv
                csv_path = ""
                for f in os.listdir(folder_path):
                    if f.lower().startswith(file_stem.lower()) and f.lower().endswith("original.csv"):
                        csv_path = os.path.join(folder_path, f)
                        break
                if not csv_path:
                    print(f"❌ No original CSV for '{file_stem}' in {folder_path}")

                match["xml_path"] = xml_path
                match["csv_path"] = csv_path

    return data

def main():
    if not os.path.exists(JSON_PATH):
        print(f"❌ JSON not found: {JSON_PATH}")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    enriched = enrich_matches(data)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2)

    print("✅ Enrichment complete. JSON updated with xml_path and csv_path.")

if __name__ == "__main__":
    main()
