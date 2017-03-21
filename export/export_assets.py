# Alex Geoffrey
# CIS 322
# export_assets.py

import psycopg2
import sys
import csv
from datetime import datetime

conn = psycopg2.connect(dbname = sys.argv[1], host = '127.0.0.1')
cur = conn.cursor()

# Get asset_tag, description, facility, aquired, disposed
cur.execute("SELECT a.tag, a.description, f.code, a.arrival_dt, a.dispose_dt FROM assets a JOIN facilities f ON a.facility_fk = f.facility_pk ORDER BY a.tag ASC")
assets = cur.fetchall()

# Create new/overwrite CSV, load in assets
with open('assets.csv','w') as newCSV:
    wr = csv.writer(newCSV, quoting=csv.QUOTE_ALL)

    # Title line
    wr.writerow(["asset_tag","description","facility","aquired_dt","disposal_dt"])
    
    # Iterate through all existing assets in DB
    for asset in assets:
        arrivalISO = datetime.isoformat(asset[3])

        # For optional: If exists, make into iso format
        if (asset[4] != None):
            disposeISO = datetime.isoformat(asset[4])
        else:
            disposeISO = "NULL"
   
        newRow = [asset[0], asset[1], asset[2], arrivalISO, disposeISO]
        wr.writerow(newRow)

# Get username, password, role and active status
cur.execute("SELECT username, password, roles.rolename, isActive FROM users JOIN roles ON roles.roles_pk = users.role_fk")
users = cur.fetchall()

# Create new/overwrite CSV file
with open('users.csv','w') as userCSV:
    wr = csv.writer(userCSV, quoting=csv.QUOTE_ALL)

    # Title row
    wr.writerow(["username","password","role","isActive"])

    # Iterate through each user in DB
    for user in users:
        wr.writerow(user)

# Get codes and names
cur.execute("SELECT code, name FROM facilities")
facs = cur.fetchall()

# Create new/overwrite CSV file
with open('facilities.csv','w') as facCSV:
    wr = csv.writer(facCSV, quoting=csv.QUOTE_ALL)
    
    # Title row
    wr.writerow(["fcode","name"])

    # Iterate through all facilities in DB
    for fac in facs:
        wr.writerow(fac)

# Get all transfer data
cur.execute("SELECT assets.tag, r.username, transfers.submit_dt, a.username, transfers.approve_dt, s.code, d.code, transfers.load_dt, transfers.unload_dt FROM transfers JOIN users r ON r.user_pk = transfers.requester_fk JOIN users a ON a.user_pk = transfers.approver_fk JOIN facilities s ON s.facility_pk = transfers.source_fk JOIN facilities d ON d.facility_pk = transfers.dest_fk JOIN assets ON assets.assets_pk = transfers.asset_fk")
transfers = cur.fetchall()

# Create new/overwrite CSV file
with open('transfers.csv','w') as transCSV:
    wr = csv.writer(transCSV, quoting=csv.QUOTE_ALL)

    # Title row
    wr.writerow(["asset_tag","request_by","request_dt","approve_by","approve_dt","source","destination","load_dt","unload_dt"])
    
    # Iterate through all transfers
    for transfer in transfers:

        # Make all optional dates either NULL or ISO format
        reqISO = datetime.isoformat(transfer[2])
        if (transfer[4] != None):
            appISO = datetime.isoformat(transfer[4])
        else:
            appISO = "NULL"
        
        if (transfer[7] != None):
            loadISO = datetime.isoformat(transfer[7])
        else:
            loadISO = "NULL"
        
        if (transfer[8] != None):
            unloadISO = datetime.isoformat(transfer[8])
        else:
            unloadISO = "NULL"

        wr.writerow([transfer[0],transfer[1], reqISO, transfer[3], appISO, transfer[5], transfer[6], loadISO, unloadISO])


