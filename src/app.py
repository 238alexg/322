# Alex Geoffrey
# Assignment 3
# app.py
# Flask python web application

from flask import Flask, render_template, request, redirect
from config import dbname, dbhost, dbport, lost_pub
from datetime import datetime
import json
import psycopg2
import sys
import os

app = Flask(__name__, template_folder='templates')
conn = psycopg2.connect(dbname=dbname, host=dbhost)
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

@app.route('/rest', methods = ['GET','POST'])
def restMenu():
    return render_template('restMenu.html')

@app.route('/rest/lost_key', methods = ['GET','POST'])
def lost_key():
    if request.method=='POST':
        dat = dict()
        dat['timestamp'] = datetime.utcnow().isoformat()
        if (lost_pub != None):
            dat['result'] = 'OK'
            dat['key'] = lost_pub
        else:
            dat['result'] = 'FAIL'
            dat['key'] = 'FAIL'

        data = json.dumps(dat)
        return data
    else:
        return redirect('/rest')

# Give user access/creates a new user and gives them access
@app.route('/rest/activate_user', methods = ['GET','POST'])
def activate_user():
    # Try to handle as plaintext
    if request.method=='POST':
        req=json.loads(request.form['activate_user'])

        dat = dict()
        dat['timestamp'] = datetime.utcnow().isoformat()

        if (req['username'] != None):
            cur.execute("SELECT * FROM users WHERE users.username = '" + req['username'] + "'")
            user = cur.fetchone()
            if (user == None):
                cur.execute("INSERT INTO users (username, active) VALUES (%s, %s)", (req['username'],"TRUE")) 
            else:
                cur.execute("UPDATE users SET active = 'TRUE' WHERE username = '" + req['username'] + "';")
            conn.commit()
            dat['result'] = 'OK'
        else:
            dat['result'] = 'FAIL'

        data = json.dumps(dat)
        return data

    else:
        return redirect('/rest')

# Suspends user access
@app.route('/rest/suspend_user', methods=['POST'])
def suspend_user():
    # Try to handle as plaintext
    if request.method=='POST':
        req=json.loads(request.form['suspend_user'])
        print (req)
        dat = dict()
        dat['timestamp'] = datetime.utcnow().isoformat()
        dat['result'] = 'OK'

        if (req['username'] != None):
            cur.execute("SELECT * FROM users WHERE users.username = '" + req['username'] + "'")
            user = cur.fetchone()
            if (user != None):
                cur.execute("UPDATE users SET active = 'FALSE' WHERE username = '" + req['username'] + "';")
                conn.commit()

        data = json.dumps(dat)
        return data

    else:
        return redirect('/rest')

@app.route('/rest/list_products', methods = ['GET','POST'])
def list_products():
    """This function is huge... much of it should be broken out into other supporting
        functions"""
    
    # Check maybe process as plaintext
    if request.method=='POST':
        req=json.loads(request.form['list_products'])
    # Unmatched, take the user somewhere else
    else:
        return redirect('/rest')
    
    # If execution gets here we have request json to work with
    # Do I need to handle compartments in this query?
    if len(req['compartments'])==0:
        print("have not compartment")
        # Just handle vendor and description
        SQLstart = """select vendor,description,string_agg(c.abbrv||':'||l.abbrv,',')
            from products p
            left join security_tags t on p.product_pk=t.product_fk
            left join compartments c on t.compartment_fk=c.compartment_pk
            left join levels l on t.level_fk=l.level_pk"""
        if req['vendor']=='' and req['description']=='':
            # No filters, add the group by and query is ready to go
            SQLstart += " group by vendor,description"
            cur.execute(SQLstart)
        else:
            if not req['vendor']=='' and not req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                req['description']="%"+req['description']+"%"
                SQLstart += " where description ilike %s and vendor ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['description'],req['vendor']))
            elif req['vendor']=='':
                req['description']="%"+req['description']+"%"
                SQLstart += " where description ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['description'],))
            elif req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                SQLstart += " where vendor ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['vendor'],))
    else:
        print("have compartment %s"%len(req['compartments']))
        # Need to handle compartments too
        SQLstart = """select vendor,description,string_agg(c.abbrv||':'||l.abbrv,',')
            from security_tags t
            left join compartments c on t.compartment_fk=c.compartment_pk
            left join levels l on t.level_fk=l.level_pk
            left join products p on t.product_fk=p.product_pk
            where product_fk is not NULL and c.abbrv||':'||l.abbrv = ANY(%s)"""
        if req['vendor']=='' and req['description']=='':
            # No filters, add the group by and query is ready to go
            SQLstart += " group by vendor,description,product_fk having count(*)=%s"
            cur.execute(SQLstart,(req['compartments'],len(req['compartments'])))
        else:
            if not req['vendor']=='' and not req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                req['description']="%"+req['description']+"%"
                SQLstart += " and description ilike %s and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['description'],req['vendor'],len(req['compartments'])))
            elif req['vendor']=='':
                req['description']="%"+req['description']+"%"
                SQLstart += " and description ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['description'],len(req['compartments'])))
            elif req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                SQLstart += " and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['vendor'],len(req['compartments'])))
    
    # One of the 8 cases should've run... process the results
    dbres = cur.fetchall()
    listing = list()
    for row in dbres:
        e = dict()
        e['vendor'] = row[0]
        e['description'] = row[1]
        if row[2] is None:
            e['compartments'] = list()
        else:
            e['compartments'] = row[2].split(',')
        listing.append(e)
    
    # Prepare the response
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['listing'] = listing
    data = json.dumps(dat)

    return data

@app.route('/rest/add_products', methods = ['GET','POST'])
def add_products():
    # Try to handle as plaintext
    if request.method=='POST':
        req=json.loads(request.form['add_products'])

        dat = dict()
        dat['timestamp'] = datetime.utcnow().isoformat()
        dat['result'] = 'OK'

        newProducts = req['new_products']
        for product in newProducts:
            print (product)
            cur.execute("SELECT * FROM products WHERE products.vendor = '" + product['vendor'] + "' AND products.description = '" + product['description'] + "';")
            prod = cur.fetchone()
            if (prod != None):
                dat['result'] = 'FAIL'
            else:
                cur.execute("INSERT INTO products (vendor, description, alt_description) VALUES (%s, %s, %s)", (product['vendor'],product['description'],product['alt_description']))
        
        conn.commit()
        data = json.dumps(dat)
        return data

    else:
        return redirect('/rest')

@app.route('/rest/add_asset', methods = ['GET','POST'])
def add_asset():
    # Try to handle as plaintext
    if request.method=='POST':
        req=json.loads(request.form['add_asset'])

        dat = dict()
        dat['timestamp'] = datetime.utcnow().isoformat()

        cur.execute("SELECT * FROM products WHERE products.vendor = '" + req['vendor'] + "' AND products.description = '" + req['description'] + "';")
        prod = cur.fetchone()
        if (prod == None):
            dat['result'] = 'FAIL'
        else:
            cur.execute("INSERT INTO assets (product_fk, description, alt_description) VALUES (%s, %s, %s)", (prod[0], req['description'], req['compartments']))
            conn.commit()
            dat['result'] = 'OK'
        
        data = json.dumps(dat)
        return data

    else:
        return redirect('/rest')

@app.route('/logout', methods = ['GET','POST'])
def logout():
	return render_template('logout.html')


app.run(host='0.0.0.0', port=8080)



