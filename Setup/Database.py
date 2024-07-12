# Setup Root Path
import sys
sys.path.append('/root/PostOffice')

# Import Packages
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from Setup.Config import APP_Settings

# Define Database Connection
SQLALCHEMY_DATABASE_URL = f'postgresql://{APP_Settings.DB_USERNAME}:{APP_Settings.DB_PASSWORD}@{APP_Settings.DB_HOSTNAME}:{APP_Settings.DB_PORT}/{APP_Settings.DB_NAME}'

# Create Database Engine
DB_Engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=30, max_overflow=10)

# Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=DB_Engine)

# Define Base Class
Base = declarative_base()

# Define Session Scope
@contextmanager
def DB_Session_Scope():

	# Create Session
	db = SessionLocal()

	try:

		# Return Session
		yield db

		# Commit Changes
		db.commit()

	except:
		
		# Rollback Changes
		db.rollback()

	finally:

		# Close Database
		db.close()