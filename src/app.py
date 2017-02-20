from flask import Flask, render_template, request, redirect
from config import dbname, dbhost, dbport
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
            if (user != None):
                return render_template('login.html', error="User already exists!")
            else:
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (loginUN, password))
                cur.commit()
                return redirect('/home/' + loginUN)

    else if (request.method == 'GET'):

   
   return render_template('login.html')



@app.route('/create_user', methods=['POST'])
def create_user():
    if (request.method == 'POST'):
        # COPY FROM LOGIN
    else:
        redirect('/login')


app.run(host='0.0.0.0', port='8080')


