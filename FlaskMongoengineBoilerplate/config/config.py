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
FRONTEND_DOMAIN = os.environ["FRONTEND_DOMAIN"] if os.getenv("FRONTEND_DOMAIN") else "http://127.0.0.1/"


# MAIL SETTINGS
EMAIL_USER = os.environ['EMAIL_USER']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
MAIL_SETTINGS = {
    "MAIL_SERVER": 'smtp.gmail.com', # Replace with smtp.sendgrid.net (For Usign Send Grid)
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": EMAIL_USER, # Replace with "apikey", and send MAIL_DEFAULT_SENDER key with value EMAIL_USER (For Send Grid)
    "MAIL_PASSWORD": EMAIL_PASSWORD
    # "MAIL_DEFAULT_SENDER": EMAIL_USER
}


FIREBASE_CONFIG = {
    "type": os.environ['type'],
    "project_id": os.environ['project_id'],
    "StorageBucket": os.environ['StorageBucket'],
    "private_key_id": os.environ['private_key_id'],
    "private_key": os.environ['private_key'],
    "client_email": os.environ['client_email'],
    "client_id": os.environ['client_id'],
    "auth_uri": os.environ['auth_uri'],
    "token_uri": os.environ['token_uri'],
    "auth_provider_x509_cert_url": os.environ['auth_provider_x509_cert_url'],
    "client_x509_cert_url": os.environ['client_x509_cert_url']
}


GOOGLE_CONFIG = {
      "web": {
        "client_id": "",
        "project_id": "",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "",
        "get_user_info_uri": "https://www.googleapis.com/oauth2/v2/userinfo",
        "redirect_uris": [
          "http://localhost:3000/login/google/callback",
        ],
        "javascript_origins": [
          "http://127.0.0.1:5000"
        ]
      }
}

FACEBOOK_CONFIG = {
    "web": {
        "client_id": "",
        "client_secret": "",
        "token_uri": "https://graph.facebook.com/v12.0/oauth/access_token",
        "get_user_info_uri": "https://graph.facebook.com/v12.0/me",
        "redirect_uris": [
          "http://localhost:5000/login/facebook/callback"
        ]
    }
}

APPLE_CONFIG = {
    "client_id": "",
    "client_secret": "",
    "private_key": "",
    "team_id": "",
    "key_id": "",
    "token_uri": "https://appleid.apple.com/auth/token",
    "client_secret_uri": "https://appleid.apple.com",
    "redirect_uris": ['http://localhost:3000/user/signup/apple']
}
