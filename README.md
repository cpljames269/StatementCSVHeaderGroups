# StatementCSVHeaderGroups
Automates ingestion, validation, normalization, grouping, enrichment, and deployment of CSV and XML statement data into a structured JSON format for a FastAPI web app. Includes scripts for folder management, CSV header extraction, fuzzy matching, and final JSON generation to support dynamic web app data loading.



✅ Full Workflow Overview ✅
This outlines the complete process for ingesting, organizing, grouping, and deploying CSV data for the FastAPI web app.

 Prep Stage: Initial Ingestion
1. 📁 Automatically Copy Incoming Folders 📁
Source:
\\192.168.2.2\Design\HOA Admin\hoa_v2\01_wip

Destination:
C:\testing

Triggered by:
Task Scheduler script (e.g., Oct_Archive_Extract.py)

The script is located at C:\testing. Make whatever changes are needed and run it to copy from the network.




2. 🗑️ Delete Unwanted Folders 🗑️
Script: delete_towne_folders.py

Location: C:\testing

What it does:
Deletes any folder whose name contains:
Towne, Resort, Sienna, Vesta




3. 🔍 Identify and Move Valid Statement Folders 🔎
Script: move_statements_folders.py

Location: C:\testing

What it does:

Scans each folder in C:\testing

Parses XML to verify it's a Statements from CSV job

Moves valid folders into:
C:\testing\statements



4. 📋 Copy CSV Headers Only 📋
Script: copy_CSVs_only_header_remaining.py

Location: C:\testing\statements\Template Creator

What it does:

Scans all CSVs in C:\testing\statements

Extracts only the first row (headers)

Saves header-only CSVs to:
C:\testing\statements\Template Creator



5. ➕➕Normalize and Copy Valid CSVs ➕➕
Script: trim_and_copy_valid_csvs.py

Location: C:\testing\statements\Template Creator

What it does:

Scans folders in C:\testing\statements

Uses fuzzy matching to find "Beginning Balance Amount" column

Trims each CSV to relevant columns and saves to:
C:\testing\statements\Template Creator\Trimmed

Filenames follow format: foldername_filename.csv

Skips or logs invalid files to log.txt




6. 📁 Group Trimmed CSVs by Header 📁
Script: grouper.py

Location: C:\testing\statements\Template Creator\Trimmed

What it does:

Groups CSVs with identical headers

Moves them into subfolders:
Group 1, Group 2, etc.
Repeat until no CSVs remain in the root of Trimmed




7. 🛠️ Build Grouped JSON Metadata 🛠️
Script: build_grouped_json_from_trimmed.py

Location: C:\testing\statements\Template Creator\Trimmed

What it does:

Parses filenames like foldername_filename.csv

Extracts:

customer_name and hoa_name from XML

original_header from source CSV

Builds:
csv_header_groups.json



8. 🧪 Enrich JSON with File Paths 🧪
Script: enrich_grouped_json_with_paths.py

Location: C:\testing\statements\Template Creator\Trimmed

What it does:

Adds:

xml_path: Full path to original XML

csv_path: Full path to original CSV

Move the resulting csv_header_groups.json to:
C:\testing\statements





9. 🧬 Match Customers to Known Clients 🧬
Script: interactive_exceldata_match_to_headersCSV.py

Location: C:\testing\statements

What it does:

Fuzzy-matches customer_name in csv_header_groups.json against clients_filtered.csv

Prompts user to confirm or override matches

Saves result as:
confirmed_matches.json




10. ✨ Apply Confirmed Matches ✨
Script: combine_confirmed_matches_with_csv_header_groups.py

Location: C:\testing\statements

What it does:

Loads:

csv_header_groups.json

confirmed_matches.json

Updates groups with confirmed mappings

Outputs final:
csv_header_groups.json




11. 🌐 Deploy JSON to Web App 🌐
Action:
Move csv_header_groups.json into:
C:\testing\app\static

Purpose:
Web app will load this enriched and confirmed file automatically.





12. 🔧 Fix Group Order for Browser 🔧
Script: Re-OrderCSV.py

Location: C:\testing\app\static

What it does:

Sorts group labels numerically (e.g., Group 10 after Group 9)

Outputs:
rename-to-csv_header_groups.json
Rename this file to "csv_header_groups.json" and delete the old one.
