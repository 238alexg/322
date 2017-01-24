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
        cur.execute("INSERT INTO assets (product_fk, asset_tag, description, alt_description) VALUES (NULL, %s, %s, %s)", (row[0],row[1],row[3]))
print("DC assets added!")

# Read in data from HQ_inventory
firstline = True
with open('osnap_legacy/HQ_inventory.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if (firstline):
            firstline = False
            continue
        cur.execute("INSERT INTO assets (product_fk, asset_tag, description, alt_description) VALUES (NULL, %s, %s, %s)", (row[0],row[1],row[3]))
print("HQ assets added!")

# Read in data from MB005_inventory
firstline = True
with open('osnap_legacy/MB005_inventory.csv') as csvfile:
	cur.execute("SELECT product_pk FROM products WHERE description = '1L H2O'")
	H20 = cur.fetchone()[0]
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if (firstline):
            firstline = False
            continue
        cur.execute("INSERT INTO assets (product_fk, asset_tag, description, alt_description) VALUES (%s, %s, %s, %s)", (H20, row[0],row[1],row[3]))
print("MB005 assets added!")

# Read in data from MB005_inventory
firstline = True
with open('osnap_legacy/MB005_inventory.csv') as csvfile:
	cur.execute("SELECT product_pk FROM products WHERE description = 'notepad'")
	notepad = cur.fetchone()[0]
    reader = csv.reader(csvfile, delimiter=',')
    i = 0
    for row in reader:
        if (firstline):
            firstline = False
            continue
        if (i = 0):
        	cur.execute("INSERT INTO assets (product_fk, asset_tag, description, alt_description) VALUES (%s, %s, %s, %s)", (notepad, row[0],row[1],row[3]))
        elif (i == 1):
        	cur.execute("INSERT INTO assets (product_fk, asset_tag, description, alt_description) VALUES (%s, %s, %s, %s)", (H20, row[0],row[1],row[3]))
        else:
        	cur.execute("INSERT INTO assets (product_fk, asset_tag, description, alt_description) VALUES (%s, %s, %s)", (row[0],row[1],row[3]))
        i += 1
print("MB005 assets added!")

# Read in data from SPNV_inventory
firstline = True
with open('osnap_legacy/MB005_inventory.csv') as csvfile:
	cur.execute("SELECT FIRST(product_pk) FROM products WHERE description = 1L H20")
	pfk = cur.fetchone()[0]
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if (firstline):
            firstline = False
            continue
        cur.execute("INSERT INTO assets (product_fk, asset_tag, description, alt_description) VALUES (%s, %s, %s)", (row[0],row[1],row[3]))
print("MB005 assets added!")


conn.commit()

cur.close()
conn.close()