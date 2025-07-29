import os
import re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

# --- CONFIG ---
BASE_DIR = Path(r"C:\testing\statements\Template Creator")
REPORT_FILE = BASE_DIR / "header_differences_report.txt"
FUZZY_MATCH_THRESHOLD = 0.85  # How close two columns must be to be considered a rename


def normalize(col):
    """Basic header normalization: lowercase, strip, remove extra spaces."""
    return re.sub(r'\s+', ' ', col.strip().lower())


def load_headers():
    """Load normalized headers from all group_xxx/header.txt files."""
    headers = {}
    for folder in BASE_DIR.iterdir():
        if folder.is_dir() and folder.name.lower().startswith("group_"):
            header_file = folder / "header.txt"
            if header_file.exists():
                with open(header_file, 'r', encoding='utf-8') as f:
                    lines = [normalize(line) for line in f.readlines() if line.strip()]
                    headers[folder.name] = set(lines)
    return headers


def find_possible_renames(set_a, set_b):
    """Find similar column names with high string similarity."""
    renames = []
    for a in set_a:
        for b in set_b:
            if a != b and SequenceMatcher(None, a, b).ratio() >= FUZZY_MATCH_THRESHOLD:
                renames.append((a, b))
    return renames


def compare_headers(headers):
    """Generate a concise diff between each pair of groups."""
    comparisons = []
    groups = sorted(headers.keys())

    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            g1, g2 = groups[i], groups[j]
            h1, h2 = headers[g1], headers[g2]

            only_in_g1 = sorted(h1 - h2)
            only_in_g2 = sorted(h2 - h1)
            possible_renames = find_possible_renames(only_in_g1, only_in_g2)

            # Remove likely renames from the lists
            renamed_g1 = {a for a, _ in possible_renames}
            renamed_g2 = {b for _, b in possible_renames}
            only_in_g1 = [col for col in only_in_g1 if col not in renamed_g1]
            only_in_g2 = [col for col in only_in_g2 if col not in renamed_g2]

            if only_in_g1 or only_in_g2 or possible_renames:
                comparisons.append(f"\n{g1} vs {g2}:")

                if only_in_g1:
                    comparisons.append(f"  + Present in {g1} only:")
                    for col in only_in_g1:
                        comparisons.append(f"    - {col}")

                if only_in_g2:
                    comparisons.append(f"  + Present in {g2} only:")
                    for col in only_in_g2:
                        comparisons.append(f"    - {col}")

                if possible_renames:
                    comparisons.append("  ~ Possible renames:")
                    for a, b in possible_renames:
                        comparisons.append(f"    - {g1}: '{a}'  <-->  {g2}: '{b}'")

    return comparisons


def main():
    headers = load_headers()
    if not headers:
        print("No header.txt files found.")
        return

    diffs = compare_headers(headers)

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("HEADER DIFFERENCES REPORT\n=========================\n")
        if diffs:
            f.write("\n".join(diffs))
        else:
            f.write("All headers are identical or have no meaningful differences.\n")

    print(f"Report saved to {REPORT_FILE}")


if __name__ == "__main__":
    main()
