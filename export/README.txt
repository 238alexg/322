/import files

- export_data.sh: shell file that takes in command line input for a database name and dump directory and calls export_assets.py, then moves generated CSV files to the dump directory
-- EX: bash export_data.sh dbname dumpdir
- export_assets.py: Takes in a database name and generates CSV files based on all existing database entries.