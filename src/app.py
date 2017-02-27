from flask import Flask, session, escape, render_template, request, redirect
from config import dbname, dbhost, dbport, secret_key
import psycopg2

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
                print("USER PW:" + user[2] + ", input: " + pw)
                if (user[2] == pw):
                    session['username'] = loginUN
                    print ("LOGGED IN " + session['username'])
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

# Logs user out of the session and returns them to the login screen
@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('username', None)
    return render_template('/login.html', error="Successfully logged out!")

#app.run(host='0.0.0.0', port='8080')


