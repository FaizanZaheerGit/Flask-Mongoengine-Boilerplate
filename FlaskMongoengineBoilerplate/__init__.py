# Python imports
import logging

# Local imports
from FlaskMongoengineBoilerplate.database.database_initialization import initialize_db
from FlaskMongoengineBoilerplate.utils import constants
from FlaskMongoengineBoilerplate.config import config
from FlaskMongoengineBoilerplate.utils import firebase_utils

# Framework imports
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_mail import Mail


# application objects
app = Flask(__name__)


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    formatter = logging.Formatter(f'%(asctime)s; %(levelname)s; %(funcName)s; %(lineno)d : %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# LOGGER SETUP
app.logger = setup_logger(constants.LOG, constants.LOG_FILE, level=logging.ERROR)

CORS(app)
bcrypt = Bcrypt(app)
app.config[constants.MONGO_DB_HOST] = config.MONGO_DB_URI
firebase_app = firebase_utils.FirebaseUtils()
initialize_db(app)

# MAIL SETTINGS
app.config.update(config.MAIL_SETTINGS)
mail = Mail(app)

# IMPORTING VIEWS, FOR INITIALIZATION
from FlaskMongoengineBoilerplate.views import user_views
from FlaskMongoengineBoilerplate.views import common_views

app.register_blueprint(user_views.user_bp, url_prefix='/api/user')
app.register_blueprint(common_views.common_bp, url_prefix='/')
