# Alex Geoffrey
# Assignment 3
# app.py
# Flask python web application

from flask import Flask, render_template, request, redirect
import psycopg2
import sys
import os

dbname = sys.argv[1]

app = Flask(__name__, template_folder='templates')
conn = psycopg2.connect(dbname=dbname, host='/tmp/')
cur = conn.cursor()

cur.execute("SELECT * FROM products;")
print (cur.fetchall())

# Login Page
@app.route('/', methods=['GET','POST'])
def login():
    if (request.method == 'POST'):
        loginUN = request.form.get('username')
        pw = request.form.get('password')
        return redirect('/home/' + loginUN)
    return render_template('login.html')

@app.route('/home/<string:username>', methods = ['GET','POST'])
def home(username = "User"):
    return render_template('home.html', username=username)

@app.route('/inventory', methods = ['GET','POST'])
def inventory():
    if (request.method == 'POST'):
    	facility = request.form.get('Facility')
    	date = request.form.get('date')
    	data = []
    return render_template('inventory.html', facility=facility, date=date, rows=data)

@app.route('/transit', methods = ['GET','POST'])
def transit():
    if (request.method == 'POST'):
    	date = request.form.get('date')
    	data = []
    return render_template('transit.html', date=date, rows=data)














app.run(host='0.0.0.0', port=8080)



