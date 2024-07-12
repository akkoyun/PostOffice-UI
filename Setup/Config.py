# Setup Root Path
import sys
sys.path.append('/root/PostOffice')

# Import Packages
from pydantic_settings import BaseSettings

# Define Setting
class Settings(BaseSettings):

	# Server Settings
	SERVER_NAME: str
	PROJECT_ROOT: str

	# Database Settings
	DB_HOSTNAME: str
	DB_PORT: str
	DB_PASSWORD: str
	DB_NAME: str
	DB_USERNAME: str

	# Load env File
	model_config = {
		"env_file": "Setup/.env"
	}

# Set Setting
APP_Settings = Settings()
