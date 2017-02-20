from flask import Flask, session, render_template, request, redirect
from config import dbname, dbhost, dbport, secret_key
import psycopg2

app = Flask(__name__, template_folder='templates')
conn = psycopg2.connect(dbname=dbname, host=dbhost)
cur = conn.cursor()

# Login page
@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    if (request.method == 'POST'):
        loginUN = request.form.get('username')
        pw = request.form.get('password')
        
        # If user provided username and password
        if ((loginUN != None) & (pw != None)):
            cur.execute("SELECT * FROM users WHERE users.username = " + loginUN + ";")
            user = cur.fetchone()

            # If username exists, check password
            if (user != None):
                # Password matches form data
                if (user[2] == pw):
                    session['username'] = loginUN
                    print ("LOGGED IN " + user[1])
                    return render_template('dashboard.html', username=loginUN)
                else:
                    return render_template('login.html', error="Incorrect password!")

    else if (request.method == 'GET'):
        return render_template('login.html', error=" ")

# Route for creating new users
@app.route('/create_user', methods=['POST'])
def create_user():
    if (request.method == 'POST'):
        loginUN = request.form.get('username')
        pw = request.form.get('password')
        
        # If user provided username and password
        if ((loginUN != None) & (pw != None)):
            cur.execute("SELECT * FROM users WHERE users.username = " + loginUN + ";")
            user = cur.fetchone()

            # If username is available, create user or return with error
            if (user != None):
                return render_template('create_user.html', error="User already exists!")
            else:
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (loginUN, password))
                cur.commit()
                return redirect('dashboard.html', username=loginUN)
    else:
        return render_template('create_user.html', error=" ")

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', user=escape(session['username']))

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('username', None)
    redirect('/login', error="Successfully logged out!")

app.run(host='0.0.0.0', port='8080')


