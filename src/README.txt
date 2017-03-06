/src files:

-app.py: This file starts and runs the web application with the web framework Flask. 
-config.py: This file loads in the flask configurations from a JSON file in the wsgi directory
-templates/
	login.html: Presents the login page for users
	create_user.html: Similar to login screen, except goes to the create_user route instead of the login. Also has a role field.
	dashboard.html: Simple dashboard that greets the user with their username
	add_asset.html: Allows user to input a new asset to the database
	add_facility.html: Allows user to add a new facility to the database
	asset_report.html: Loads/posts data generating asset reports for facilities/dates
	dispose_asset.html: Allows qualified users to dispose of assets
	error.html: A generic template feeding various errors to the user. Also links back to the dashboard.
	approve_req.html: Allows Facilities Officers to approve of transit requests
	transfer_report.html: Post and displays reports for assets in transit on the given date
	transfer_req.html: Allows Logistics Officers to post requests for asset transfers
	update_transit.html: Allows Logistics Officers to update transfer's transit status
	success.html: Unused, a temporary file used during testing
