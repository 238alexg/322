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
        un = request.form.get('username')
        pw = request.form.get('password')

        print("UN: " + un, "PW: " + pw)
        return redirect('/home/' + un)

    return render_template('login.html')

@app.route('/home/<string:username>', methods = ['GET','POST'])
def home(username = "User"):
    if (request.method == 'POST'):
        print("PSOTED")
    return render_template('home.html', username=username)


app.run(host='0.0.0.0', port=8080)

