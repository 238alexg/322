import psycopg2
import sys
import csv

# Connect to the database
conn = psycopg2.connect(dbname=sys.argv[1], host='/tmp/')
cur = conn.cursor()



# Read in data from files
firstline = True

with open('osnap_legacy/product_list.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if (firstline):
            firstline = False
            continue
        print (row)
        print (row[4] + ", " + row[0] + "," + row[2])
        cur.execute("INSERT INTO products (vendor, description, alt_description) VALUES (%s, %s, %s)", (row[4],row[0],row[2]))

# Read in data from DC_inventory
firstline = True
with open('osnap_legacy/DC_inventory.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if (firstline):
            firstline = False
            continue
        cur.execute("INSERT INTO products (description, alt_description) VALUES (%s, %s)", (row[1],row[3]))
print("DC assets added!")

# Read in data from HQ_inventory
firstline = True
with open('osnap_legacy/HQ_inventory.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if (firstline):
            firstline = False
            continue
        cur.execute("INSERT INTO products (description, alt_description) VALUES (%s, %s)", (row[1],row[3]))
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
        cur.execute("INSERT INTO products (description, alt_description) VALUES (%s, %s)", (row[1],row[3]))
print("MB005 assets added!")

# Read in data from MB005_inventory
firstline = True
with open('osnap_legacy/MB005_inventory.csv') as csvfile:
    cur.execute("SELECT product_pk FROM products WHERE description = 'notepad'")
    notepad = cur.fetchone()[0]
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if (firstline):
            firstline = False
            continue
        cur.execute("INSERT INTO products (description, alt_description) VALUES (%s, %s)", (row[1],row[3]))
print("MB005 assets added!")

# Read in data from SPNV_inventory
firstline = True
with open('osnap_legacy/MB005_inventory.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if (firstline):
            firstline = False
            continue
        cur.execute("INSERT INTO products (description, alt_description) VALUES (%s, %s)", (row[1],row[3]))
print("MB005 assets added!")




conn.commit()

cur.close()
conn.close()


