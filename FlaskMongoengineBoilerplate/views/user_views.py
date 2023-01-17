# Python imports

# Framework imports
from flask import jsonify, request

# Local imports
from FlaskMongoengineBoilerplate import app
from FlaskMongoengineBoilerplate.controllers import user_controller
from FlaskMongoengineBoilerplate.utils import responses, decorators, constants, common_utils


@app.route("/api/user/create", methods=["POST"])
@decorators.logging
@decorators.validator(required_fields=[constants.NAME, constants.EMAIL_ADDRESS, constants.PASSWORD, constants.GENDER],
                      optional_fields=[constants.DATE_OF_BIRTH, constants.IMAGE])
def create_user_view(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    user, response_code, response_message = user_controller.create_user_controller(data)
    response_obj = {}
    if response_code != responses.CODE_SUCCESS:
        response_obj = responses.get_response_object(response_code=response_code,
                                                     response_message=response_message)
    elif response_code == responses.CODE_SUCCESS:
        response_obj = responses.get_response_object(response_code=response_code,
                                                     response_data={"user": user},
                                                     response_message=response_message)
    return jsonify(response_obj)


@app.route("/api/user/read", methods=["GET"])
@decorators.logging
def read_user_view():
    """
    This API reads a new user,
    optional filters can be used, for filtering data of users
    :param:
    :return:
    """
    data = common_utils.get_posted_data(method="GET")
    users, response_code, response_message = user_controller.read_user_controller(data)
    response_obj = {}
    if response_code != responses.CODE_SUCCESS:
        response_obj = responses.get_response_object(response_code=response_code,
                                                     response_message=response_message)
    elif response_code == responses.CODE_SUCCESS:
        response_obj = responses.get_response_object(response_code=response_code,
                                                     response_data={"users": users},
                                                     response_message=response_message)
    return jsonify(response_obj)


@app.route("/api/user/update", methods=["PUT"])
@decorators.logging
@decorators.is_authenticated
@decorators.validator(required_fields=[constants.UID],
                      optional_fields=[constants.NAME, constants.GENDER, constants.DATE_OF_BIRTH, constants.STATUS, constants.IMAGE])
def update_user_view(data):
    """
    This API updates a users data
    :param data:
    :return:
    """
    user, response_code, response_message = user_controller.update_user_controller(data)
    response_obj = {}
    if response_code != responses.CODE_SUCCESS:
        response_obj = responses.get_response_object(response_code=response_code,
                                                     response_message=response_message)
    elif response_code == responses.CODE_SUCCESS:
        response_obj = responses.get_response_object(response_code=response_code,
                                                     response_data={"user": user},
                                                     response_message=response_message)
    return jsonify(response_obj)


@app.route("/api/user/delete/<uid>", methods=["DELETE"])
@decorators.logging
@decorators.is_authenticated
def delete_user_view(uid):
    """
    This API deletes a user
    :param uid:
    :return:
    """
    response_code, response_message = user_controller.delete_user_controller(uid)
    response_obj = responses.get_response_object(response_code=response_code,
                                                 response_message=response_message)
    return jsonify(response_obj)


@app.route("/api/user/login", methods=["POST"])
@decorators.logging
@decorators.validator(required_fields=[constants.EMAIL_ADDRESS, constants.PASSWORD], optional_fields=[])
def login_view(data):
    """
    This API logins a user, based on email address and password
    :param data:
    :return:
    """
    user, token, response_code, response_message = user_controller.login_user_controller(data)
    response_obj = {}
    if response_code != responses.CODE_SUCCESS:
        response_obj = responses.get_response_object(response_code=response_code,
                                                     response_message=response_message)
    elif response_code == responses.CODE_SUCCESS:
        response_obj = responses.get_response_object(response_code=response_code,
                                                     response_data={"user": user,
                                                                    "session-key": token},
                                                     response_message=response_message)
    return jsonify(response_obj)


@app.route("/api/user/logout", methods=["POST"])
@decorators.logging
@decorators.is_authenticated
def logout_view():
    """
    This API logouts an authenticated user
    :param:
    :return:
    """
    token = request.headers.get("session-key", None)
    response_code, response_message = user_controller.logout_user_controller(token)
    response_obj = responses.get_response_object(response_code=response_code,
                                                 response_message=response_message)
    return jsonify(response_obj)


@app.route("/api/upload/<_type>", methods=["POST"])
@decorators.logging
def upload_image_view(_type):
    """
    This API uploads an image to firebase storage bucket
    :param:
    :return:
    """
    image = common_utils.get_posted_files().get(constants.IMAGE)

    url, response_code, response_message = user_controller.upload_image_controller(_file=image, _type=_type)
    response_obj = {}
    if response_code != responses.CODE_SUCCESS:
        response_obj = responses.get_response_object(response_code=response_code,
                                                     response_message=response_message)
    elif response_code == responses.CODE_SUCCESS:
        response_obj = responses.get_response_object(response_code=response_code,
                                                     response_data={"url": url},
                                                     response_message=response_message)
    return jsonify(response_obj)
