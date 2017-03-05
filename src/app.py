from flask import Flask, session, escape, render_template, request, redirect
from config import dbname, dbhost, dbport, secret_key
import psycopg2
from datetime import datetime

app = Flask(__name__, template_folder='templates')
conn = psycopg2.connect(dbname=dbname, host=dbhost)
cur = conn.cursor()

# Set secret key
app.secret_key = secret_key

# Login page: logs in user or redirects them to the create_user page if no user found
@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    if (request.method == 'POST'):
        loginUN = request.form.get('username')
        pw = request.form.get('password')

        # If user provided username and password
        if ((loginUN != "") & (pw != "")):
            cur.execute("SELECT * FROM users WHERE users.username = \'" + loginUN + "\';")
            user = cur.fetchone()

            # If username exists, check password
            if (user != None):
                # Password matches form data
                if (user[2] == pw):
                    session['username'] = loginUN
                    return redirect('/dashboard')
                else:
                    return render_template('login.html', error="Incorrect password!")
            else:
                return render_template('/create_user.html', error="User doesn't exist. Create new user below!")
        else:
            return render_template('login.html', error="Cannot log in with blank username or password. If you want to create a new user, type in any input and press login, and you will be taken to the page. Alternatively, visit localhost:8080/create_user")

    return render_template('login.html', error=" ")

# Route for creating new users. If user already exists, loads error into html
@app.route('/create_user', methods=['GET','POST'])
def create_user():
    if (request.method == 'POST'):
        loginUN = request.form.get('username')
        pw = request.form.get('password')
        role = request.form.get('role')

        # If user provided username and password
        if ((loginUN != "") & (pw != "")):
            cur.execute("SELECT * FROM users WHERE users.username = \'" + loginUN + "\';")
            user = cur.fetchone()

            # If username is available, create user or return with error
            if (user != None):
                return render_template('create_user.html', error="User already exists!")
            
            # If role is entered, try to find it in DB
            elif (role != None):
                cur.execute("SELECT * FROM roles WHERE roles.rolename = \'" + role + "\'")
                userRole = cur.fetchone()
                
                # If not found, create it before inserting new user
                if (userRole == None):
                    cur.execute("INSERT INTO roles (rolename) VALUES (\'" + role + "\')")
                    cur.execute("SELECT * FROM roles WHERE roles.rolename = \'" + role + "\'")
                    userRole = cur.fetchone()
                
                # Insert new user
                cur.execute("INSERT INTO users (username, password, role_fk) VALUES (%s, %s, %s)", (loginUN, pw, str(userRole[0])))
            # If creating user with no role, don't give user a role
            else:
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (loginUN, pw))

            # Commit changes, login user
            conn.commit()
            session['username'] = loginUN
            return redirect('/dashboard')
        else:
            return render_template('create_user.html', error="Cannot have blank username or password!")
    
    print("GOT HERE")
    return render_template('create_user.html', error=" ")

# Route that presents incrediably simple dashboard with the user's username, and logout button
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', username=session['username'])

# Route to add a facility
@app.route('/add_facility', methods=['GET','POST'])
def add_facility(error=""):
    # If just visiting page
    if (request.method == 'GET'):
        # Get all existing facilities form the DB
        cur.execute("SELECT * FROM facilities;")
        facilities = cur.fetchall()
        # Load them into the page
        return render_template('add_facility.html', facilities=facilities, error=error)
    
    # If adding a facility
    elif (request.method == 'POST'):
        # Get form data
        facilityName = request.form.get('facilityName')
        facilityCode = request.form.get('facilityCode')

        # Get the facility with that name
        cur.execute("SELECT * FROM facilities WHERE (name = \'" + facilityName + "\' OR code = \'" + facilityCode + "\')")
        facility = cur.fetchone()

        # Facility already exists
        if (facility != None):
            return render_template('error.html',error="Facility already exists!")
        # If facility doesn't exist yet, add to the DB
        else:
            cur.execute("INSERT INTO facilities (name, code) VALUES (%s, %s)", (facilityName, facilityCode))
            conn.commit()
            return redirect('/add_facility')

# Route to add an asset
@app.route('/add_asset', methods=['GET','POST'])
def add_asset():
    # If visiting page
    if (request.method == 'GET'):
        # Get all the facility names
        cur.execute("SELECT name FROM facilities;")
        facilityNames = cur.fetchall()
        # And load them into the page
        return render_template('add_asset.html', facilities=facilityNames)
    
    # If trying to add an asset
    elif (request.method == 'POST'):
        # Get form data
        assetTag = request.form.get('assetTag')
        assetDesc = request.form.get('assetDesc')
        facilityName = request.form.get('facility')
        rawtime = request.form.get('date')
        dtobj = datetime.strptime(rawtime, "%Y-%m-%d" + "T" + "%H:%M")

        # Get asset with same tag, if any
        cur.execute("SELECT * FROM assets WHERE tag = \'" + assetTag + "\'")
        asset = cur.fetchone()

        # If found asset with the same tag already, error
        if (asset != None):
            return render_template('error.html', error="Asset with tag " + assetTag + " already exists!")
        
        # Otherwise add this asset to the DB
        else: 
            cur.execute("SELECT facility_pk FROM facilities WHERE facilities.name = \'" + facilityName + "\'")
            facilityFK = cur.fetchone()
            cur.execute("INSERT INTO assets (tag, description, facility_fk, arrival_dt) VALUES (%s, %s, %s, %s)", (assetTag, assetDesc, facilityFK, dtobj))
            conn.commit()
            return redirect('/add_asset')

# Route to dispose of an asset
@app.route('/dispose_asset', methods=['GET','POST'])
def dispose_asset():
    # Get logged in user's UN
    loginUN = session['username']

    # Find user's role in the DB
    cur.execute("SELECT roles.rolename FROM users, roles WHERE (users.username = \'" + loginUN + "\' AND users.role_fk = roles.roles_pk)")
    role = cur.fetchone()

    # If they don't have the correct role, error
    if (role[0] != "Logistics Officer"):
        return render_template("error.html", error="User's role must be Losgistics Officer in order to modify assets")
    
    # If visiting page, load vanilla page
    elif (request.method == 'GET'):
        return render_template('dispose_asset.html')
    
    # If trying to dispose of an asset
    elif (request.method == 'POST'):
        # Get form data
        tag = request.form.get('assetTag')
        rawdt = request.form.get('date')
        dtobj = datetime.strptime(rawdt, "%Y-%m-%d" + "T" + "%H:%M")

        # Find asset to dispose of
        cur.execute("SELECT * FROM assets WHERE assets.tag = \'" + tag + "\'")
        asset = cur.fetchone()

        # If asset found
        if (asset != None):
            # If it is already disposed of, error
            if (asset[3] == None):
                return render_template('error.html', error="Asset already disposed")
            # Else, update with disposed facility (NULL) and form date
            else:
                cur.execute("UPDATE assets SET facility_fk = NULL, arrival_dt = %s WHERE assets.tag = %s", (dtobj, tag))
        # Asset not found, error
        else:
            return render_template('error.html', error="Asset does not exist!")

        # Save changes and redirect to dashboard
        conn.commit()
        return redirect('/dashboard')

# Route to report assets from a given day
@app.route('/asset_report', methods=['GET','POST'])
def asset_report():
    # Get facility names for loading into page
    cur.execute("SELECT facilities.name FROM facilities")
    facilityNames = cur.fetchall()

    # If visiting page, load page
    if (request.method == 'GET'):
        return render_template('asset_report.html', facilities=facilityNames)
    
    # If generating a report
    elif (request.method == 'POST'):
        # Get form data
        facility = request.form.get('facility')
        rawdate = request.form.get('date')
        dtobj = datetime.strptime(rawdate, "%Y-%m-%d" + "T" + "%H:%M")
        print (dtobj)

        # If no facility indicated, load all assets from DB where arrival date is BEFORE date on form (already arrived)
        if (facility == "All"):
            cur.execute("SELECT * FROM assets WHERE assets.arrival_dt <= %s", [dtobj])
            print("GOT HERE")
        
        # Else do above only with assets from given facility
        else:
            cur.execute("SELECT facilities.facility_pk FROM facilities WHERE facilities.name = \'" + facility + "\'")
            fpk = cur.fetchone()
            cur.execute("SELECT * FROM assets WHERE (assets.arrival_dt <= %s AND assets.facility_fk = %s)", (dtobj, fpk))

        # Load report results and facility names into the page
        assets = cur.fetchall()
        print (assets)
        return render_template('asset_report.html', assets=assets, facilities=facilityNames)

# Logs user out of the session and returns them to the login screen
@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('username', None)
    return render_template('/login.html', error="Successfully logged out!")

# When not using mod-wsgi, uncomment below
#app.run(host='0.0.0.0', port='8080')


