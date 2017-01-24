# Alex Geoffrey
# Assignment 2
# Insert asset instances to database


import sys
import psycopg2
import csv

# Connect to the database
conn = psycopg2.connect(dbname=sys.argv[1], host='/tmp/')
cur = conn.cursor()

# Read in data from DC_inventory
firstline = True

with open('osnap_legacy/DC_inventory.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if (firstline):
            firstline = False
            continue
        print(row)
        cur.execute("INSERT INTO assets (product_fk, asset_tag, description, alt_description) VALUES (NULL, %s, %s, %s)", (row[0],row[1],row[3]))
