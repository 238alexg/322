/import files

- import_data.sh: shell file that takes in command line input for dbname and input directory and calls imports.py
-- EX: bash import_data.sh dbname inputdir
- imports.py: Takes in a database name and a directory name, and imports CSV file data from that directory into the database