# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Libraries
from flask import Flask, render_template
from Setup import Database, Models
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

# Create Flask App
app = Flask(__name__)



# Get All Variables
def Get_All_Variables():

	# Try to open a database session
	try:

		# Open a database session
		with Database.DB_Session_Scope() as DB:

			# Query all data types
			Query_Log = DB.query(Models.Log).order_by(desc(Models.Log.Create_Time)).limit(20).all()

			# Set Data Type List
			Data_Type_List = [
				{
					'Log_ID': Log.Log_ID,
					'Log_Level_ID': Log.Log_Level_ID,
					'Log_Description_ID': Log.Log_Description_ID,
					'Service_ID': Log.Service_ID,
					'Device_ID': Log.Device_ID,
					'Log_Message': Log.Log_Message,
				} for Log in Query_Log
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
	return render_template("home.html", Variables=Variables, name='Gunce')





# Run the App
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)