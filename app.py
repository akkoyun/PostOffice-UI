# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Libraries
from flask import Flask, render_template
from Setup import Database, Models
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
			Query_Variables = DB.query(Models.Variable).all()

			# Set Data Type List
			Data_Type_List = {Variable.Variable_ID: Variable.Variable_Unit for Variable in Query_Variables}

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