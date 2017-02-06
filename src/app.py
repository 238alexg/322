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
    month = request.form.get('Month')
    day = request.form.get('Day')
    year = request.form.get('Year')

    date = year + "-" + month + "-" + day
    facs = ["DC","HQ","MB005","NC","SPNV"]

    print (date)
    
    # If facility not specified
    if ((facility == "All") | (facility == None)):
    	# If only date
    	print("No facility: ", facility)
    	cur.execute(('''SELECT assets.description, fcode, arrive_dt, depart_dt 
    		    	FROM asset_at 
       	    		INNER JOIN facilities ON asset_at.facility_fk = facilities.facility_pk 
    			INNER JOIN assets ON asset_at.asset_fk = assets.asset_pk
	    		WHERE asset_at.arrive_dt ''' + "<= \'" + date + "\' AND asset_at.depart_dt is NULL;"))
    	facility = "All Facilities"
    # If both date and facility specified
    else:
    	print("Facility and date: ", facility)
    	cur.execute(('''SELECT assets.description, fcode, arrive_dt, depart_dt 
    				FROM asset_at 
       				INNER JOIN facilities ON asset_at.facility_fk = facilities.facility_pk 
    				INNER JOIN assets ON asset_at.asset_fk = assets.asset_pk
                                WHERE asset_at.facility_fk = ''' + facility + " AND asset_at.arrive_dt <= \'" + date + "\' AND asset_at.depart_dt is NULL;"))
    	facility = facs[int(facility)-1]

    data = cur.fetchall()

    return render_template('inventory.html', facility=facility, date=date, rows=data)

@app.route('/transit', methods = ['GET','POST'])
def transit():
    month = request.form.get('Month')
    day = request.form.get('Day')
    year = request.form.get('Year')

    date = year + "-" + month + "-" + day
    print (date)
    
    cur.execute(('''SELECT assets.description, fcode, arrive_dt, depart_dt 
		    	FROM asset_at 
   	    		INNER JOIN facilities ON asset_at.facility_fk = facilities.facility_pk 
    			INNER JOIN assets ON asset_at.asset_fk = assets.asset_pk
                        WHERE ''' + "(asset_at.depart_dt is NULL AND asset_at.arrive_dt >= \'" + date + "\') OR asset_at.depart_dt <= \'" + date + "\';"))

    data = cur.fetchall()
    return render_template('transit.html', date=date, rows=data)


@app.route('/logout', methods = ['GET','POST'])
def logout():
	return render_template('logout.html')


app.run(host='0.0.0.0', port=8080)



