#!/usr/bin/bash

# Alex Geoffrey
# Assignment 2
# Import_Data.sh

# Curls legacy data for LOST
curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > legacy_data.tar.gz

# Unpack files to /osnap_legacy
tar -xvzf legacy_data.tar.gz

# Create tables with sql script
psql $1 -f create_tables.sql

# Insert product into into rows
python3 insert_products.py $1
python3 insert_assets.py $1
python3 insert_facilities.py $1
python3 insert_asset_at.py $1
python3 insert_levels.py $1
python3 insert_compartments.py $1

# Destroy legacy data
rm -R osnap_legacy

# DEBUG: Destroy tables
#psql $1 -f destroy_tables.sql
