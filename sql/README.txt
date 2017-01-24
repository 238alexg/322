This directory holds some tools for configuring the LOST database and migrating legacy OSNAP data.

Files:

import_data.sh - Downloads legacy files, calls sql script to create tables, and inserts data by calling python scripts

create_tables.sql - sql script that creates all the tables in the LOST PDF

insert_asset_at.py - inserts and commits asset_ats into the database
insert_levels.py - inserts and commits levels into the database
insert_assets.py - inserts and commits assets into the database
insert_products.py - inserts and commits products into the database
destroy_tables.sql - Mostly for testing, wipes database
insert_compartment.py - inserts and commits compartments into the database
insert_facilities.py - inserts and commits facilities into the database

README.txt - This readme file
logfile - Just some fatal errors from building code logged here
