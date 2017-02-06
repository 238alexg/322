Alex Geoffrey
CIS 322 at the University of Oregon

Top-level files
install_daemons.sh - Bash script that downloads and installs apache and postgres
preflight.sh - Bash script that creates and populates database by taking 1 argument of database name. Also copies all files in src to both the ../wsgi folder and a seperate folder (for easier commits), and starts the Flask application.

322/src
- This directory holds a flask application as well as templates folder for html pages
Files:
- app.py - Runs the flask application, performs psql queries, gives data to Jinja2 to put into html format
- /templates
	- login.html - A simple login page that posts without validation.
	- home.html - The filter screen for psql queries about inventory/transit.
	- inventory.html - The page wherein inventory queries are loaded and presented.
	- transit.html - The page wherein transit queries are loaded and presented.
	- logout.html - A very simple logout page with a button to log back in.

322/sql
- This directory holds some tools for configuring the LOST database and migrating legacy OSNAP data.
Files:
- import_data.sh - Downloads legacy files, calls sql script to create tables, and inserts data by calling python scripts
- create_tables.sql - sql script that creates all the tables in the LOST PDF
- insert_asset_at.py - inserts and commits asset_ats into the database
- insert_levels.py - inserts and commits levels into the database
- insert_assets.py - inserts and commits assets into the database
- insert_products.py - inserts and commits products into the database
- destroy_tables.sql - Mostly for testing, wipes database
- insert_compartment.py - inserts and commits compartments into the database
- insert_facilities.py - inserts and commits facilities into the database