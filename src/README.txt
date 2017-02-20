/src files:

-app.py: This file starts and runs the web application with the web framework Flask. 
-config.py: This file loads in the flask configurations from a JSON file in the wsgi directory
-templates/
	login.html: Presents the login page for users
	create_user.html: Similar to login screen, except goes to the create_user route instead of the login.
	dashboard.html: Simple dashboard that greets the user with their username
