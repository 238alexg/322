Alex Geoffrey
CIS 322 at the University of Oregon

INSTRUCTIONS TO RUN: 
- Use the command "./preflight DBNAME", where DBNAME is the name of your database
- The script also starts the Flask application, no need to do anything else
- Go to "localhost:8080" on your browser
- Have fun :)

Of note:
322/preflight.sh - Bash script that creates and populates database by taking 1 argument of database name. Also copies all files in src to both the ../wsgi folder and a seperate folder (for easier commits), and starts the Flask application.

322/src
- This directory holds a flask application as well as templates folder for html pages
Files:
- app.py - Runs the flask application, performs psql queries, gives data to Jinja2 to put into html format
- /templates
	- login.html - A simple login page that posts without validation.
	- home.html - The filter screen for psql queries about inventory/transit.
	- inventory.html - The page wherein inventory queries are loaded and presented.
	- transit.html - The page wherein transit queries are loaded and presented.
	- logout.html - A very simple logout page with a button to log back in
	- restMenu.html - A page describing/posting to all the RESTful API stubs in the application