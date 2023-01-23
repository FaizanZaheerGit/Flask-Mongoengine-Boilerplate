# Python Imports
import jwt
import uuid

# Framework Imports
from flask import request, g

# Local Imports
from FlaskMongoengineBoilerplate import app
from FlaskMongoengineBoilerplate.database import database_layer
from FlaskMongoengineBoilerplate.config import config
from FlaskMongoengineBoilerplate.models import token_model
from FlaskMongoengineBoilerplate.utils import constants, common_utils, user_utils


def generate_session_token(user):
    """
    This function generates a new session token for logging a user
    :return token:
    """
    token_jwt = jwt.encode(payload={"user": user_utils.get_user_object(user=user)}, key="secret", algorithm="HS256")
    token_jwt = common_utils.convert_byte_to_string(token_jwt)
    token = str(token_jwt) + "-" + str(uuid.uuid4())

    insert_filter = {constants.USER: user, constants.TOKEN: token, constants.PURPOSE: constants.SESSION_MANAGEMENT,
                     constants.EXPIRY_TIME: config.SESSION_EXPIRATION_TIME}
    database_layer.insert_record(collection=token_model.Token, data=insert_filter)

    return token


def check_current_user():
    """
    This function checks the session token of a user
    :param:
    :return:
    """
    current_token = request.headers.get("session-key", None)
    if not current_token:
        print("Token not found in headers")
        return

    token_object = database_layer.read_single_record(collection=token_model.Token,
                                                     read_filter={constants.TOKEN: current_token,
                                                                  constants.PURPOSE: constants.SESSION_MANAGEMENT,
                                                                  constants.EXPIRY_TIME: config.SESSION_EXPIRATION_TIME,
                                                                  constants.IS_EXPIRED: False})

    if not token_object:
        print('Invalid session token')
        return

    current_user = token_object[constants.USER]
    if current_user:
        set_current_user(user=current_user)
    else:
        print("User not found")

    return current_user


def set_current_user(user):
    """
    This function sets a user as current
    :param user:
    :return:
    """
    return g.setdefault(constants.USER, user)


def get_current_user():
    """
    This function gets current user of session
    :return:
    """
    return g.get(constants.USER, None)


def destroy_user_session_tokens(user, purpose=constants.SESSION_MANAGEMENT):
    """
    This function will destroy tokens of a user
    :param user:
    :param purpose:
    :return:
    """
    database_layer.modify_records(collection=token_model.Token,
                                  read_filter={constants.USER: user,
                                               constants.PURPOSE: purpose,
                                               constants.IS_EXPIRED: False},
                                  update_filter={constants.EXPIRY_TIME: common_utils.get_current_time(),
                                                 constants.IS_EXPIRED: True})
    return


def expire_token(token):
    """
    This function expires a specific token
    :param token:
    :return:
    """
    database_layer.modify_records(collection=token_model.Token,
                                  read_filter={constants.TOKEN: token},
                                  update_filter={constants.EXPIRY_TIME: common_utils.get_current_time(),
                                                 constants.IS_EXPIRED: True,
                                                 constants.UPDATED_AT: common_utils.get_current_time()})
    return


def generate_forgot_password_verification_url(user):
    """
    This function generates a verification url and e-mails it to the user for resetting pasword
    :param user:
    :return verification_url as a string:
    """
    destroy_user_session_tokens(user=user, purpose=constants.FORGOT_PASSWORD)
    token_value = str(uuid.uuid4())

    insert_filter = {constants.USER: user, constants.TOKEN: token_value, constants.PURPOSE: constants.FORGOT_PASSWORD,
                     constants.EXPIRY_TIME: config.SESSION_EXPIRATION_TIME}

    token = database_layer.insert_record(collection=token_model.Token,
                                         data=insert_filter)

    verification_link_url = config.FRONTEND_DOMAIN + f"/reset-password/{user.uid}/{token[constants.TOKEN]}"
    return verification_link_url
