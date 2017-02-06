# Alex Geoffrey
# Assignment 3
# app.py
# Flask python web application

from flask import Flask, render_template, request, redirect
import psycopg2
import sys
import os
from datetime import datetime

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
    facility = request.form.get('Facility')
    month = int(request.form.get('Month'))
    day = int(request.form.get('Day'))
    year = int(request.form.get('Year'))

    date = datetime(year, month, day, 0, 0, 0, 0)

    # If facility not specified
    if ((facility == "All") | (facility == None)):
    	# If there are no parameters for the query
    	if ((date == None) | (date == "")):
    		print("No facility or date: ", facility, date)
    		cur.execute('''SELECT assets.description, fcode, arrive_dt, depart_dt 
    				FROM asset_at
       				INNER JOIN facilities ON asset_at.facility_fk = facilities.facility_pk 
    				INNER JOIN assets ON asset_at.asset_fk = assets.asset_pk;''')
    	# If only date was specified
    	else:
    		print("No facility: ", facility, date)
    		cur.execute(('''SELECT assets.description, fcode, arrive_dt, depart_dt 
    				FROM asset_at 
       				INNER JOIN facilities ON asset_at.facility_fk = facilities.facility_pk 
    				INNER JOIN assets ON asset_at.asset_fk = assets.asset_pk
    				WHERE asset_at.arrive_dt > (%s)-(%s)-(%s)::date;''', year, month, day))
    
    # If only Facility was specified
    elif (date == None):
    	print("No date: ", facility, date)
    	cur.execute(('''SELECT assets.description, fcode, arrive_dt, depart_dt 
    				FROM asset_at 
       				INNER JOIN facilities ON asset_at.facility_fk = facilities.facility_pk 
    				INNER JOIN assets ON asset_at.asset_fk = assets.asset_pk
    				WHERE asset_at.facility_fk = (%s);''', facility))

    # If both date and facility specified
    else :
    	print("Facility and date: ", facility, date)
    	cur.execute(('''SELECT assets.description, fcode, arrive_dt, depart_dt 
    				FROM asset_at 
       				INNER JOIN facilities ON asset_at.facility_fk = facilities.facility_pk 
    				INNER JOIN assets ON asset_at.asset_fk = assets.asset_pk
    				WHERE asset_at.facility_fk = (%s) AND asset_at.arrive_dt > (%s)-(%s)-(%s)::date;''', facility, year, month, day))
    data = cur.fetchall()
    print(data)

    return render_template('inventory.html', facility=facility, date=date, rows=data)

@app.route('/transit', methods = ['GET','POST'])
def transit():
    if (request.method == 'POST'):
    	date = request.form.get('date')
    	data = []
    return render_template('transit.html', date=date, rows=data)


@app.route('/logout', methods = ['GET','POST'])
def logout():
	return render_template('logout.html')


app.run(host='0.0.0.0', port=8080)



