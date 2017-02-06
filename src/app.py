# Alex Geoffrey
# Assignment 3
# app.py
# Flask python web application

from flask import Flask, render_template
import psycopg2
import sys
import os


dbname = sys.argv[1]
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__), 'templates')

app = Flask(__name__, template_folder='/templates')
conn = psycopg2.connect(dbname=dbname, host='/tmp/')
cur = conn.cursor()

cur.execute("SELECT * FROM products;")
print (cur.fetchall())

# Login Page
@app.route('/', methods=['GET','POST'])
def login():
    return render_template('login.html')

app.run(host='0.0.0.0', port=8080)

