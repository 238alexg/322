# Alex Geoffrey
# Assignment 2
# Insert facility instances to database

import sys
import psycopg2
import csv

# Connect to the database
conn = psycopg2.connect(dbname=sys.argv[1], host='/tmp/')
cur = conn.cursor()

# There is literally real data about the facilities common_name or location, 
# so I don't even think I should do this, but:
cur.execute("INSERT INTO facilities (fcode, location) VALUES (%s, %s)", ("DC","Washington, D.C."))
cur.execute("INSERT INTO facilities (fcode, location) VALUES (%s, %s)", ("HQ", "Headquarters"))
cur.execute("INSERT INTO facilities (fcode) VALUES (%s)","MB005")
cur.execute("INSERT INTO facilities (fcode, location) VALUES (%s, %s)", ("NC", "National City"))
cur.execute("INSERT INTO facilities (fcode, location) VALUES (%s, %s)", ("SPNV","Sparks, NV"))

conn.commit()

cur.close()
conn.close()
