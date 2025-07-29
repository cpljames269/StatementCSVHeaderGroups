import json
import csv
from thefuzz import process, fuzz

JSON_FILE = 'csv_header_groups.json'
CSV_FILE = 'clients_filtered.csv'
CONFIRMED_MATCHES_FILE = 'confirmed_matches.json'

def load_json_customer_names(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    names = set()
    for group in data:
        # Each group has subgroups, each with matches
        if "subgroups" in group:
            for subgroup in group["subgroups"]:
                for entry in subgroup['matches']:
                    names.add(entry['customer_name'].lower().strip())
        else:
            # fallback for old format
            for entry in group.get('matches', []):
                names.add(entry['customer_name'].lower().strip())
    return list(names)

def load_csv_clients(csv_path):
    clients = {}
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clients[row['Client Name'].lower().strip()] = row
    return clients

def interactive_match(json_names, csv_clients):
    csv_names = list(csv_clients.keys())
    confirmed = {}

    for name in json_names:
        best_match, score = process.extractOne(name, csv_names, scorer=fuzz.token_sort_ratio)
        print(f"\nJSON Customer Name: {name}")
        print(f"Best CSV match: {best_match} (score: {score})")

        while True:
            ans = input("Is this a correct match? (y/n): ").strip().lower()
            if ans == 'y':
                confirmed[name] = best_match
                break
            elif ans == 'n':
                print("Other possible matches:")
                matches = process.extract(name, csv_names, scorer=fuzz.token_sort_ratio, limit=5)
                for i, (m, s) in enumerate(matches):
                    print(f"{i+1}: {m} (score: {s})")
                choice = input("Enter number to select a different match or 'skip' to skip: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= 5:
                    confirmed[name] = matches[int(choice)-1][0]
                    break
                elif choice.lower() == 'skip':
                    print("Skipping match for this name.")
                    break
            else:
                print("Please answer with 'y' or 'n'.")

    with open(CONFIRMED_MATCHES_FILE, 'w', encoding='utf-8') as f:
        json.dump(confirmed, f, indent=2)
    print(f"\nSaved confirmed matches to {CONFIRMED_MATCHES_FILE}")

if __name__ == "__main__":
    json_names = load_json_customer_names(JSON_FILE)
    csv_clients = load_csv_clients(CSV_FILE)
    interactive_match(json_names, csv_clients)
