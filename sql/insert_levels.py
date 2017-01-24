#Alex Geoffrey
#Assignment 2
# Insert_Security Levels

import psycopg2
import sys
import csv

# Connect to the database
conn = psycopg2.connect(dbname=sys.argv[1], host='/tmp/')
cur = conn.cursor()



# Read in data from file
firstline = True

with open('osnap_legacy/security_levels.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if (firstline):
            firstline = False
            continue
        cur.execute("INSERT INTO levels (abbrv, comment) VALUES (%s, %s)", (row[0],row[1]))

conn.commit()

cur.close()
conn.close()


