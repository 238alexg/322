# Alex Geoffrey
# Assignment 2
# Insert asset_at instances to database


import sys
import psycopg2
import csv
import datetime

# Connect to the database
conn = psycopg2.connect(dbname=sys.argv[1], host='/tmp/')
cur = conn.cursor()

# Read in data from DC_inventory
firstline = True
with open('osnap_legacy/DC_inventory.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    cur.execute("SELECT facility_fk FROM facilities WHERE fcode = DC")
    facility = cur.fetchone()[0]
    for row in reader:
        if (firstline):
            firstline = False
            continue
        cur.execute("SELECT asset_pk FROM assets WHERE description = %s",(row[1]))
        asset = cur.fetchone()[0]
        arrival = datetime.datetime.strptime(row[4])
        cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES (%s, %s, %s)", (asset,facility, arrival)) 

# Read in data from HQ_inventory
firstline = True
with open('osnap_legacy/HQ_inventory.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    cur.execute("SELECT facility_fk FROM facilities WHERE fcode = HQ")
    facility = cur.fetchone()[0]
    for row in reader:
        if (firstline):
            firstline = False
            continue
        cur.execute("SELECT asset_pk FROM assets WHERE description = %s",(row[1]))
        asset = cur.fetchone()[0]
        arrival = datetime.datetime.strptime(row[4])
        cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES (%s, %s, %s)", (asset,facility, arrival)) 

# Read in data from MB005_inventory
firstline = True
with open('osnap_legacy/MB005_inventory.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    cur.execute("SELECT facility_fk FROM facilities WHERE fcode = MB005")
    facility = cur.fetchone()[0]
    for row in reader:
        if (firstline):
            firstline = False
            continue
        cur.execute("SELECT asset_pk FROM assets WHERE description = %s",(row[1]))
        asset = cur.fetchone()[0]
        arrival = datetime.datetime.strptime(row[4])
        departure = datetime.datetime.strptime(row[5])
        cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt, depart_dt) VALUES (%s, %s, %s, %s)", (asset,facility, arrival, departure)) 

# Read in data from MB005_inventory
firstline = True
with open('osnap_legacy/NC_inventory.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    cur.execute("SELECT facility_fk FROM facilities WHERE fcode = NC")
    facility = cur.fetchone()[0]
    for row in reader:
        if (firstline):
            firstline = False
            continue
        cur.execute("SELECT asset_pk FROM assets WHERE description = %s",(row[1]))
        asset = cur.fetchone()[0]
        arrival = datetime.datetime.strptime(row[4])
        if (i < 3):
            departure = datetime.datetime.strptime(row[5])
            cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt, depart_dt) VALUES (%s, %s, %s, %s)", (asset,facility, arrival, departure)) 
        else:
            cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_d) VALUES (%s, %s, %s)", (asset,facility, arrival)) 

# Read in data from SPNV_inventory
firstline = True
with open('osnap_legacy/SPNV_inventory.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    cur.execute("SELECT facility_fk FROM facilities WHERE fcode = DC")
    facility = cur.fetchone()[0]
    for row in reader:
        if (firstline):
            firstline = False
            continue
        cur.execute("SELECT asset_pk FROM assets WHERE description = %s",(row[1]))
        asset = cur.fetchone()[0]
        arrival = datetime.datetime.strptime(row[4])
        cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES (%s, %s, %s)", (asset,facility, arrival)) 


conn.commit()

cur.close()
conn.close()
