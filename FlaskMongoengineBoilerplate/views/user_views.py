# Python imports

# Framework imports
from flask import request, Blueprint

# Local imports
from FlaskMongoengineBoilerplate import app
from FlaskMongoengineBoilerplate.controllers import user_controller
from FlaskMongoengineBoilerplate.utils import responses, decorators, constants, common_utils


user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/create', methods=["POST"])
@decorators.logging
@decorators.validator(required_fields=[constants.NAME, constants.EMAIL_ADDRESS, constants.PASSWORD, constants.GENDER],
                      optional_fields=[constants.DATE_OF_BIRTH, constants.IMAGE])
def create_user_view(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return user_controller.create_user_controller(data)


@user_bp.route('/read', methods=["GET"])
@decorators.logging
def read_user_view():
    """
    This API reads a new user,
    optional filters can be used, for filtering data of users
    :param:
    :return:
    """
    data = common_utils.get_posted_data(method="GET")
    return user_controller.read_user_controller(data)


@user_bp.route('/update', methods=["PUT"])
@decorators.logging
@decorators.is_authenticated
@decorators.validator(required_fields=[constants.ID],
                      optional_fields=[constants.NAME, constants.GENDER, constants.DATE_OF_BIRTH, constants.STATUS, constants.IMAGE])
def update_user_view(data):
    """
    This API updates a users data
    :param data:
    :return:
    """
    return user_controller.update_user_view(data)


@user_bp.route('/delete/<id>', methods=["DELETE"])
@decorators.logging
@decorators.is_authenticated
def delete_user_view(id):
    """
    This API deletes a user
    :param id:
    :return:
    """
    return user_controller.delete_user_controller(id)


@user_bp.route('/login', methods=["POST"])
@decorators.logging
@decorators.validator(required_fields=[constants.EMAIL_ADDRESS, constants.PASSWORD], optional_fields=[])
def login_view(data):
    """
    This API logins a user, based on email address and password
    :param data:
    :return:
    """
    return user_controller.login_user_controller(data)


@user_bp.route('/logout', methods=["GET", "POST"])
@decorators.logging
@decorators.is_authenticated
def logout_view():
    """
    This API logouts an authenticated user
    :param:
    :return:
    """
    token = request.headers.get("session-key", None)
    return user_controller.logout_user_controller(token)


@user_bp.route('/forgot-password', methods=["PATCH"])
@decorators.logging
@decorators.validator([constants.EMAIL_ADDRESS])
def forgot_password(data):
    """
    This API will take e-mail of a user as a parameter
    and will send a verification URL containing the id and a token, to the email in case of a forgotten password
    :param data:
    :return:
    """
    return user_controller.forgot_password_email(data[constants.EMAIL_ADDRESS])


@user_bp.route("/reset-password", methods=['PATCH'])
@decorators.logging
@decorators.validator([constants.ID, constants.TOKEN, constants.NEW_PASSWORD])
def user_change_password_token(data):
    """
    This is change password in case of forgotten password,
    and will update the password of a user using the token in the verification link
    :param data:
    :return:
    """
    return user_controller.change_password_by_token(data[constants.ID], data[constants.TOKEN],
                                                    data[constants.NEW_PASSWORD])


@user_bp.route("/change-password", methods=["PATCH"])
@decorators.logging
@decorators.is_authenticated
@decorators.validator([constants.ID, constants.OLD_PASSWORD, constants.NEW_PASSWORD])
def change_password_view(data):
    """
    This API will take id of a user, and will update the password of a user and set it to the new password
    :param data:
    :return:
    """
    return user_controller.change_password_controller(data[constants.ID], data[constants.OLD_PASSWORD],
                                                      data[constants.NEW_PASSWORD])


@user_bp.route("/upload/<_type>", methods=["POST"])
@decorators.logging
def upload_image_view(_type):
    """
    This API uploads an image to firebase storage bucket
    :param:
    :return:
    """
    image = common_utils.get_posted_files().get(constants.IMAGE)
    return user_controller.upload_image_controller(_file=image, _type=_type)


@user_bp.route("/social/signup/<_type>", methods=["POST"])
@decorators.logging
@decorators.validator([constants.OAUTH_CODE])
def social_oauth_signup(data, _type):
    """
    This API will log in a user through social media accounts
    :param data:
    :param _type:
    :return:
    """
    oauth_code = data[constants.OAUTH_CODE]
    name = data.get(constants.NAME, None)
    return user_controller.social_signup_controller(oauth_code, _type, name)


@user_bp.route("/social/login/<_type>", methods=["POST"])
@decorators.logging
@decorators.validator([constants.OAUTH_CODE])
def social_oauth_login(data, _type):
    oauth_code = data[constants.OAUTH_CODE]
    return user_controller.social_login_controller(oauth_code=oauth_code, _type=_type)
