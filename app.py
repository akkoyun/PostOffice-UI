# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Libraries
from flask import Flask, render_template
from Setup import Database, Models
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

# Create Flask App
app = Flask(__name__)



# Get All Variables
def Get_All_Variables():

	# Try to open a database session
	try:

		# Open a database session
		with Database.DB_Session_Scope() as DB:

			# Query all data types
			Query_Log = DB.query(Models.Log).options(
					joinedload(Models.Log.level),
					joinedload(Models.Log.description),
					joinedload(Models.Log.service),
				).order_by(desc(Models.Log.Create_Time)).limit(10).all()

			# Set Badge Classes
			service_badge_classes = {
				1: 'badge-primary',
				2: 'badge-secondary',
				3: 'badge-success',
				4: 'badge-danger',
				5: 'badge-warning',
				6: 'badge-info',
				7: 'badge-light',
				8: 'badge-dark'
			}




			# Set Data Type List
			Data_Type_List = [
				{
					'Create_Time': log.Create_Time,
					'Device_Name': log.device.Device_Name,
					'Log_Level_Name': log.level.Log_Level_Name,
					'Service_Name': log.service.Service_Name,
					'Log_Description_Name': log.description.Log_Description_Name,
					'Service_Badge_Class': service_badge_classes.get(log.Service_ID, 'badge-primary'),
				} for log in Query_Log
			]

			# Get Data Type List
			return Data_Type_List

	# Handle Exceptions
	except SQLAlchemyError as e:

		# Return Empty Dictionary
		return {}

Variables = Get_All_Variables()





@app.route("/")
def hello():
	return render_template("home.html", Variables=Variables)





# Run the App
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)