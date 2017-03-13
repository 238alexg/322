# Alex Geoffrey
# CIS 322
# imports.py


import psycopg2
import datetime
import sys
import csv

conn = psycopg2.connect(dbname = sys.argv[1], host="127.0.0.1")
cur = conn.cursor()

# IMPORT USERS
firstline = True
with open(sys.argv[2] + "/users.csv") as userCSV:
    reader = csv.reader(userCSV, delimiter=',')
    for row in reader:
        # Do not include title row
        if (firstline):
            firstline = False
            continue
        
        # Get user role
        cur.execute("SELECT * FROM roles WHERE roles.rolename = '" + row[2] + "'")
        role = cur.fetchone()

        # Insert role if it doesn't exist
        if (role == None):
            cur.execute("INSERT INTO roles (rolename) VALUES ('" + row[2] + "')")
            cur.execute("SELECT * FROM roles WHERE roles.rolename = '" + row[2] + "'")
            role = cur.fetchone() 
        
        # Once role exists in DB, insert user
        cur.execute("INSERT INTO users (username, password, role_fk, isActive) VALUES (%s, %s, %s, %s)",(row[0], row[1], role[0], row[3]))

conn.commit()


# IMPORT FACILITIES
firstline = True
with open(sys.argv[2] + "/facilities.csv") as facCSV:
    reader = csv.reader(facCSV, delimiter=',')
    for row in reader:
        # Do not include title row
        if (firstline):
            firstline = False
            continue

        cur.execute("INSERT INTO facilities (code, name) VALUES (%s, %s)",(row[0],row[1]))

conn.commit()


# IMPORT ASSETS
firstline = True
with open(sys.argv[2] + "/assets.csv") as assetCSV:
    reader = csv.reader(assetCSV, delimiter=',')
    for row in reader:
        # Do not include title row
        if (firstline):
            firstline = False
            continue

        # Get facility key
        cur.execute("SELECT facility_pk FROM facilities WHERE facilities.code = '" + row[2] + "'")
        fac = cur.fetchone()
        
        # If dispose time is not "NULL", pad with single quotes for DB insertion
        if (row[4] != "NULL"):
            aquire_dt = "'" + row[4] + "'"
        else:
            aquire_dt = row[4]
        
        cur.execute("INSERT INTO assets (tag, description, facility_fk, arrival_dt, dispose_dt) VALUES (%s, %s, %s, %s, " + aquire_dt + ")",(row[0], row[1], fac[0], row[3]))

conn.commit()



# IMPORT TRANSFERS
firstline = True
with open(sys.argv[2] + "/transfers.csv") as transCSV:
    reader = csv.reader(transCSV, delimiter=',')
    for row in reader:
        # Do not include title row
        if (firstline):
            firstline = False
            continue
        
        # Find asset
        cur.execute("SELECT assets.assets_pk FROM assets WHERE assets.tag = '" + row[0] + "'")
        asset = cur.fetchone()

        # Find requester and approver (if not "NULL")
        if (row[3] != "NULL"):
            cur.execute("SELECT r.user_pk, a.user_pk FROM users JOIN users r ON r.username = '" + row[1] + "' JOIN users a ON a.username = '" + row[3] + "'")
            users = cur.fetchone()
            reqUser = users[0]
            appUser = "'" + str(users[1]) + "'"
        else:
            cur.execute("SELECT user_pk FROM users WHERE users.username = '" + row[1] + "'")
            users = cur.fetchone()
            reqUser = users[0]
            appUser = row[3]

        # Pad optional datetimes with single quotes if they are not null
        if (row[4] != "NULL"):
            approve_dt = "'" + row[4] + "'"
        else:
            approve_dt = row[4]

        if(row[7] != "NULL"):
            load_dt = "'" + row[7] + "'"
        else:
            load_dt = row[7]

        if (row[8] != "NULL"):
            unload_dt = "'" + row[8] + "'"
        else:
            unload_dt = row[8]

        # Find souce and destination facilities
        cur.execute("SELECT s.facility_pk, d.facility_pk FROM facilities JOIN facilities s ON s.code = '" + row[5] + "' JOIN facilities d ON d.code = '" + row[6] + "'")
        facs = cur.fetchone()
        source = facs[0]
        dest = facs[1]

        cur.execute("INSERT INTO transfers(requester_fk, submit_dt, source_fk, load_dt, dest_fk, unload_dt, asset_fk, approver_fk, approve_dt) VALUES (%s, %s, %s, " + load_dt + ", %s, " + unload_dt + ", %s, " + appUser + ", " + approve_dt + ")", (reqUser, row[2], source, dest, asset[0]))


conn.commit()



