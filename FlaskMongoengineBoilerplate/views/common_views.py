# Python imports

# Framework imports
from flask import jsonify, Blueprint

# Local imports
from FlaskMongoengineBoilerplate import app
from FlaskMongoengineBoilerplate.config import static_data
from FlaskMongoengineBoilerplate.utils import responses, decorators


common_bp = Blueprint('common_bp', __name__)


@common_bp.route("/", methods=["GET"])
@decorators.logging
def server_check():
    return "Server is up and running."


@common_bp.route("/api/static-data", methods=["GET"])
@decorators.logging
def get_static_data_view():
    """
    This API returns static data
    :param:
    :return:
    """
    static = static_data.get_static_data()

    response_obj = responses.get_response_object(responses.CODE_SUCCESS,
                                                 {"static_data": static},
                                                 responses.MESSAGE_SUCCESS)
    return jsonify(response_obj)
