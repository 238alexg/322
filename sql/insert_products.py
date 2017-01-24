import psycopg2
import sys
import csv

# Connect to the database
print (sys.argv[0])
print (sys.argv[1])
print (sys.argv[2])

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=int(sys.argv[2]))
cur = conn.cursor()

# Read in data from files
with open('osnap_legacy/product_list.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        cur.execute("INSERT INTO products VALUES (%s)", (row[4] + "," + row[0] + "," + row[2]))

print ("\nProduct Inserts complete!\n")



