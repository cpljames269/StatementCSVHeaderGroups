import json
import csv

CSV_HEADER_GROUPS_JSON = 'csv_header_groups.json'
CSV_CLIENTS_CSV = 'clients_filtered.csv'
CONFIRMED_MATCHES_JSON = 'confirmed_matches.json'
OUTPUT_JSON = 'rename_to-csv_header_groups.json'

def normalize_key(name):
    if not name:
        return ""
    return name.lower().strip().replace('–', '-')

def load_csv_clients(csv_path):
    clients = {}
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = normalize_key(row['Client Name'])
            clients[key] = row
    return clients

def load_confirmed_matches(matches_path):
    with open(matches_path, 'r', encoding='utf-8') as f:
        raw_matches = json.load(f)
    # Normalize keys and values
    return {
        normalize_key(k): normalize_key(v)
        for k, v in raw_matches.items()
    }

def enrich_json(json_path, clients, confirmed_matches):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for group in data:
        # Handle nested structure with subgroups
        if "subgroups" in group:
            for subgroup in group["subgroups"]:
                for entry in subgroup['matches']:
                    cust_name = normalize_key(entry.get('customer_name'))
                    matched_client_name = confirmed_matches.get(cust_name)

                    if matched_client_name:
                        client_info = clients.get(matched_client_name)
                        if client_info:
                            entry['Client ID'] = client_info.get('Client ID', '')
                            entry['Bank(s)'] = client_info.get('Bank(s)', '')
                            entry['Software(s)'] = client_info.get('Software(s)', '')
                        else:
                            print(f"❌ No match in CSV for: '{matched_client_name}'")
                    else:
                        print(f"⚠️ No confirmed match for: '{cust_name}'")
        else:
            # Fallback for old flat structure
            for entry in group.get('matches', []):
                cust_name = normalize_key(entry.get('customer_name'))
                matched_client_name = confirmed_matches.get(cust_name)

                if matched_client_name:
                    client_info = clients.get(matched_client_name)
                    if client_info:
                        entry['Client ID'] = client_info.get('Client ID', '')
                        entry['Bank(s)'] = client_info.get('Bank(s)', '')
                        entry['Software(s)'] = client_info.get('Software(s)', '')
                    else:
                        print(f"❌ No match in CSV for: '{matched_client_name}'")
                else:
                    print(f"⚠️ No confirmed match for: '{cust_name}'")

    return data

def save_enriched_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"\n✅ Saved enriched JSON to: {output_path}")

if __name__ == "__main__":
    clients = load_csv_clients(CSV_CLIENTS_CSV)
    confirmed_matches = load_confirmed_matches(CONFIRMED_MATCHES_JSON)
    enriched_data = enrich_json(CSV_HEADER_GROUPS_JSON, clients, confirmed_matches)
    save_enriched_json(enriched_data, OUTPUT_JSON)
