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
                    
                    # Save role in session
                    cur.execute("SELECT roles.rolename FROM roles WHERE roles.roles_pk = \'" + str(user[3]) + "\';")
                    rolename = cur.fetchone()
                    session['role'] = rolename[0]

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
            session['role'] = role
            return redirect('/dashboard')
        else:
            return render_template('create_user.html', error="Cannot have blank username or password!")
    
    print("GOT HERE")
    return render_template('create_user.html', error=" ")

# Route that presents incrediably simple dashboard with the user's username, and logout button
@app.route('/dashboard/<string:message>', methods=['GET'])
@app.route('/dashboard', methods=['GET'])
def dashboard(message=''):
    if (session['role'] == "Logistics Officer"):
        # Select all asset tags from transfers without a set load to unload time
        cur.execute("SELECT assets.tag, transfers.transfer_pk FROM assets, transfers WHERE (assets.assets_pk = transfers.asset_fk) AND (transfers.unload_dt IS NULL) AND (transfers.load_dt IS NOT NULL) AND (transfers.approver_fk IS NOT NULL)")
        transfers = cur.fetchall()
        
        cur.execute("SELECT assets.tag, transfers.transfer_pk FROM assets, transfers WHERE (assets.assets_pk = transfers.asset_fk) AND (transfers.load_dt IS NULL) AND (transfers.approver_fk IS NOT NULL)")
        loadedTransfers = cur.fetchall()

        return render_template('dashboard.html', username=session['username'],role=session['role'], message=message, transfers=transfers, loadedTransfers=loadedTransfers)
    elif (session['role'] == "Facilities Officer"):
        # Select all transfers still needing approval
        cur.execute("SELECT assets.tag, facilities.name, transfers.transfer_pk FROM assets, facilities, transfers WHERE (assets.assets_pk = transfers.asset_fk) AND (facilities.facility_pk = transfers.dest_fk) AND (transfers.approver_fk IS NULL)")
        transfers = cur.fetchall()
        return render_template('dashboard.html', username=session['username'], role=session['role'], message=message, transfers=transfers)
    
    return render_template('dashboard.html', username=session['username'], role=session['role'], message=message)

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
    role = session['role']

    # If they don't have the correct role, error
    if (role != "Logistics Officer"):
        return render_template("error.html", error="User's role must be Losgistics Officer in order to modify assets")
    
    # If visiting page, load vanilla page
    elif (request.method == 'GET'):
        cur.execute("SELECT * FROM assets")
        assets = cur.fetchall()
        return render_template('dispose_asset.html', assets=assets)
    
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

# Route to initiate transit requests
@app.route('/transfer_req', methods=['GET','POST'])
def transfer_req():
    if (session['role'] != "Logistics Officer"):
        return render_template('error.html', error="Must be a Logistics Officer to initiate transfer requests!")
    elif (request.method == "GET"):
        cur.execute("SELECT facilities.name FROM facilities")
        facilities = cur.fetchall()
        cur.execute("SELECT assets.tag, facilities.name FROM assets, facilities WHERE assets.facility_fk = facilities.facility_pk")
        assets = cur.fetchall()
        return render_template('transfer_req.html', facilities=facilities, assets=assets)
    elif (request.method == "POST"):
        # Check validity of asset tag (kept as text input instead of select options since it sounded 
        # like some kind of input validation was needed)
        tag = request.form.get('tag')
        cur.execute("SELECT * FROM assets WHERE assets.tag = \'" + tag + "\';")
        asset = cur.fetchone()
        if (asset == None):
            return render_template('error.html', error="Error: Asset tag does not exist!")
        
        source = request.form.get('source')
        dest = request.form.get('dest')

        # If user tries to transfer asset to the same facility
        if (source == dest):
            return render_template('error.html', error="Source and destination cannot be the same facility!")

        # Since facilities are loaded into select from DB, they must be valid, no validation necessary
        cur.execute("SELECT facilities.facility_pk FROM facilities WHERE facilities.name = \'" + source + "\';")
        source_fk = cur.fetchone()
       
        print (source_fk)

        if (asset[3] != source_fk[0]):
            return render_template('error.html', error="Asset is not at the source facility!")
        
        cur.execute("SELECT facilities.facility_pk FROM facilities WHERE facilities.name = \'" + dest + "\';")
        dest_fk = cur.fetchone()

        curdt = datetime.now()

        cur.execute("SELECT users.user_pk FROM users WHERE users.username = \'" + session['username'] + "\';")
        user = cur.fetchone()
        
        # Insert transfer request into table and commit
        cur.execute("INSERT INTO transfers (requester_fk, submit_dt, source_fk, dest_fk, asset_fk) VALUES (%s, %s, %s, %s, %s)", (user[0], curdt, source_fk[0], dest_fk[0], asset[0]))
        conn.commit()

        return render_template("success.html", message="Transfer request for asset " + tag + " successfully submitted") 

# Route to approve of transit requests
@app.route('/approve_req/<transfer_pk>', methods=['GET'])
@app.route('/approve_req/<transfer_pk>/<approve>', methods=['POST'])
def approve_req(transfer_pk=-1, approve="True"):
    if (session['role'] != "Facilities Officer"):
        return render_template('error.html', error="Must be a Facilities Officer to approve assets!")
    elif (request.method == 'GET'):
        if (transfer_pk == -1):
            return render_template('error.html', error="Invalid transfer key! Transfer is not logged in the database!")
        else:
            cur.execute("SELECT assets.tag, facilities.name, transfers.transfer_pk FROM assets, facilities, transfers WHERE (transfers.transfer_pk = \'" + str(transfer_pk) + "\') AND (assets.assets_pk = transfers.asset_fk) AND (facilities.facility_pk = transfers.dest_fk)")
            transfer = cur.fetchone()
            return render_template('approve_req.html', transfer=transfer)
    elif (request.method == 'POST'):
        # If transfer is approved, update DB with approving user and datetime of approval
        if (approve == "True"):
            cur.execute("SELECT user_pk FROM users WHERE users.username = \'" + session['username'] + "\';")
            user_pk = cur.fetchone()[0]
            cur.execute("UPDATE transfers SET approver_fk = %s, approve_dt = %s WHERE transfers.transfer_pk = %s", (user_pk, datetime.now(), transfer_pk))
            message = "Transfer approved"
        # If transfer is not approved, remove it from the DB
        else:
            cur.execute("DELETE FROM transfers WHERE transfers.transfer_pk = \'" + str(transfer_pk) + "\';")
            message = "Transfer removed from databse"
        # Regardless of approval, save DB changes and redirect to dashboard
        conn.commit()
        return redirect('/dashboard/' + message)

# Route to set the load and unload times of approved transfer requests
@app.route('/update_transit/<transfer_pk>', methods=['GET', 'POST'])
def update_transit(transfer_pk = -1):
    if (session['role'] != "Logistics Officer"):
        return render_template('error.html', error="Only Logistics Officers can update load and unload times!")
    elif (request.method == 'GET'):
        if (transfer_pk == -1):
            return render_template('error.html', error="Invalid transfer key! Transfer does not exist in the database!")
        else:
            cur.execute("SELECT assets.tag, facilities.name, transfer_pk, transfers.load_dt FROM assets, facilities, transfers WHERE (transfers.transfer_pk = \'" + str(transfer_pk) + "\') AND (assets.assets_pk = transfers.asset_fk) AND (facilities.facility_pk = transfers.dest_fk)")
            transfer = cur.fetchone()
            cur.execute("SELECT facilities.name FROM facilities, transfers WHERE (transfers.transfer_pk = \'" + str(transfer_pk) + "\') AND (facilities.facility_pk = transfers.source_fk)")
            source = cur.fetchone()[0]
            return render_template('update_transit.html', transfer=transfer, source=source)
    elif (request.method == 'POST'):
        if (request.form.get('load_dt')):
            rawLDT = request.form.get('load_dt')
            load_dt = datetime.strptime(rawLDT, "%Y-%m-%d" + "T" + "%H:%M")
            cur.execute("UPDATE transfers SET load_dt = %s WHERE transfers.transfer_pk = %s", (load_dt, transfer_pk))
            message = "Transfer load time recorded"
        elif (request.form.get('unload_dt')):
            rawUDT = request.form.get('unload_dt')
            unload_dt = datetime.strptime(rawUDT, "%Y-%m-%d" + "T" + "%H:%M")
            cur.execute("UPDATE transfers SET unload_dt = %s WHERE transfers.transfer_pk = %s", (unload_dt, transfer_pk))
            message = "Transfer unload time recorded"
        conn.commit()
        return redirect("/dashboard/" + message)

# Route for a transfer report of all assets in transit
@app.route('/transfer_report', methods=['GET','POST'])
def transfer_report():
    if (request.method == 'GET'):
        return render_template('transfer_report.html')
    elif (request.method == 'POST'):
        rawdt = request.form.get('date')
        dtobj = datetime.strptime(rawdt, "%Y-%m-%d" + "T" + "%H:%M")
        cur.execute("SELECT assets.tag, transfers.load_dt, transfers.unload_dt FROM assets, transfers WHERE (transfers.load_dt <= %s) AND (transfers.unload_dt >= %s) AND (transfers.asset_fk = assets.assets_pk)", (dtobj, dtobj))
        results = cur.fetchall()

        return render_template('transfer_report.html', results=results)

# Logs user out of the session and returns them to the login screen
@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('username', None)
    return render_template('/login.html', error="Successfully logged out!")

# When not using mod-wsgi, uncomment below
app.run(host='0.0.0.0', port='8080')


