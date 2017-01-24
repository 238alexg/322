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


conn.commit()

cur.close()
conn.close()


