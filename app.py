# Python Imports
import os
from dotenv import find_dotenv, load_dotenv

# Framework Imports

# Local imports
from FlaskMongoengineBoilerplate import app
from FlaskMongoengineBoilerplate.config import config


def _run():
    if os.path.exists(find_dotenv()):
        load_dotenv(find_dotenv())
    else:
        print(".env file not found")
    port = os.getenv("PORT", 5000)

    """ Imports the app and runs it. """
    app.run(debug=config.APP_DEBUGGING, host="0.0.0.0", port=port)


if __name__ == '__main__':
    _run()
