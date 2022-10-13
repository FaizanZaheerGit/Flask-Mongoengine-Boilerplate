# Python imports

# Local imports
from FlaskMongoengineBoilerplate.database.database_initialization import initialize_db
from FlaskMongoengineBoilerplate.utils import constants
from FlaskMongoengineBoilerplate.config import config

# Framework imports
from flask import Flask
from flask_cors import CORS
import logging

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


app.logger = setup_logger(constants.LOG, constants.LOG_FILE, level=logging.ERROR)

CORS(app)
app.config[constants.MONGO_DB_HOST] = config.MONGO_DB_URI
initialize_db(app)


# IMPORTING VIEWS, FOR INITIALIZATION
from FlaskMongoengineBoilerplate.views import user_views
from FlaskMongoengineBoilerplate.views import common_views
