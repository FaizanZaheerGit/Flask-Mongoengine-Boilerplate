# Python imports
import os
from dotenv import load_dotenv, find_dotenv

# Local imports

if os.path.exists(find_dotenv()):
    load_dotenv(find_dotenv())
else:
    print(".env file not found")

MONGO_DB_URI = os.environ["MONGO_DB_URI"]
APP_DEBUGGING = True if os.environ['APP_DEBUGGING'].lower() == "true" else False
SESSION_EXPIRATION_TIME = 0  # SET EXPIRATION TIME IN HOURS => example 5/60 = 0.083, so 0.083 would be 5 minutes
