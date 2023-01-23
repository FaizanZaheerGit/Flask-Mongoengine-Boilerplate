# Python imports
import uuid
from datetime import datetime
import requests
import jwt
from threading import Thread

# Framework Imports

# Local imports
from FlaskMongoengineBoilerplate.database import database_layer
from FlaskMongoengineBoilerplate.models import user_model, token_model
from FlaskMongoengineBoilerplate.config import static_data, config
from FlaskMongoengineBoilerplate.utils import responses, constants, user_utils, common_utils, token_utils
from FlaskMongoengineBoilerplate import app, firebase_app


def create_user_controller(data):
    """
    This function creates a new user based on the data
    :param data:
    :return:
    """
    # TODO Validate input static dictionaries (like gender etc. )
    if type(data[constants.NAME]) != str:
        return None, responses.CODE_INVALID_DATA_TYPE, responses.MESSAGE_INVALID_DATA_TYPE.format(constants.NAME)

    if type(data[constants.PASSWORD]) != str:
        return None, responses.CODE_INVALID_DATA_TYPE, responses.MESSAGE_INVALID_DATA_TYPE.format(constants.PASSWORD)

    if type(data[constants.GENDER]) != dict:
        return None, responses.CODE_INVALID_DATA_TYPE, responses.MESSAGE_INVALID_DATA_TYPE.format(constants.GENDER)

    if data.get(constants.DATE_OF_BIRTH):
        if type(data[constants.DATE_OF_BIRTH]) != str:
            return None, responses.CODE_INVALID_DATA_TYPE, \
                responses.MESSAGE_INVALID_DATA_TYPE.format(constants.DATE_OF_BIRTH)

        valid_date = common_utils.validate_date_format(date=data[constants.DATE_OF_BIRTH])
        if not valid_date:
            return None, responses.CODE_INVALID_VALUE, \
                responses.MESSAGE_INVALID_VALUE.format(constants.DATE_OF_BIRTH) + ", use format YYYY-MM-DD"

    if data.get(constants.IMAGE):
        if type(data[constants.IMAGE]) != str:
            return None, responses.CODE_INVALID_DATA_TYPE, responses.MESSAGE_INVALID_DATA_TYPE.format(constants.IMAGE)

    if type(data[constants.EMAIL_ADDRESS]) != str:
        return None, responses.CODE_INVALID_DATA_TYPE, \
            responses.MESSAGE_INVALID_DATA_TYPE.format(constants.EMAIL_ADDRESS)

    data[constants.EMAIL_ADDRESS] = data[constants.EMAIL_ADDRESS].lower()
    valid_email = common_utils.validate_email_address(email=data[constants.EMAIL_ADDRESS])
    if not valid_email:
        return None, responses.CODE_INVALID_VALUE, responses.MESSAGE_INVALID_VALUE.format(constants.EMAIL_ADDRESS)

    existing_email_user = database_layer.read_single_record(collection=user_model.User,
                                                            read_filter={constants.EMAIL_ADDRESS:
                                                                         data[constants.EMAIL_ADDRESS]})
    if existing_email_user:
        return None, responses.CODE_ALREADY_EXISTS, \
            responses.MESSAGE_ALREADY_EXISTS.format(constants.USER, constants.EMAIL_ADDRESS)

    data[constants.PASSWORD], data[constants.PASSWORD_SALT] = common_utils.encrypt_password(
        user_password=data[constants.PASSWORD])

    new_user = database_layer.insert_record(collection=user_model.User, data=data)

    return user_utils.get_user_object(user=new_user), responses.CODE_SUCCESS, responses.MESSAGE_SUCCESS


def read_user_controller(data):
    """
    This function reads all users, using data as a filter (data can be empty)
    :param data:
    :return:
    """
    user_filter_items = [constants.NAME, constants.EMAIL_ADDRESS, constants.GENDER, constants.STATUS]
    user_filter_dict = common_utils.get_filtered_items(filter_list=user_filter_items, data=data)

    if user_filter_dict.get(constants.GENDER):
        if user_filter_dict[constants.GENDER].lower() == "male":
            user_filter_dict[constants.GENDER] = static_data.gender[0]

        elif user_filter_dict[constants.GENDER].lower() == "female":
            user_filter_dict[constants.GENDER] = static_data.gender[1]

        elif user_filter_dict[constants.GENDER].lower() == "other":
            user_filter_dict[constants.GENDER] = static_data.gender[2]

        else:
            user_filter_dict[constants.GENDER] = {}

    if user_filter_dict.get(constants.STATUS):
        if user_filter_dict[constants.STATUS].lower() == "active":
            user_filter_dict[constants.STATUS] = static_data.user_status[0]

        elif user_filter_dict[constants.STATUS].lower() == "inactive":
            user_filter_dict[constants.STATUS] = static_data.user_status[1]

        elif user_filter_dict[constants.STATUS].lower() == "suspended":
            user_filter_dict[constants.STATUS] = static_data.user_status[2]

        else:
            user_filter_dict[constants.STATUS] = {}

    user_objects = database_layer.read_record(collection=user_model.User, read_filter=user_filter_dict)
    users = user_utils.filter_user_object(users=user_objects)

    return users, responses.CODE_SUCCESS, responses.MESSAGE_SUCCESS


def update_user_controller(data):
    """
    This function updates a user, based on a read filter and update filter, sent inside data
    :param data:
    :return:
    """
    # TODO Validate input static dictionaries (like gender etc. )
    if type(data[constants.UID]) != str:
        return None, responses.CODE_INVALID_DATA_TYPE, responses.MESSAGE_INVALID_DATA_TYPE.format(constants.UID)

    if data.get(constants.NAME):
        if type(data[constants.NAME]) != str:
            return None, responses.CODE_INVALID_DATA_TYPE, responses.MESSAGE_INVALID_DATA_TYPE.format(constants.NAME)

    if data.get(constants.GENDER):
        if type(data[constants.GENDER]) != dict:
            return None, responses.CODE_INVALID_DATA_TYPE, responses.MESSAGE_INVALID_DATA_TYPE.format(constants.GENDER)

    if data.get(constants.DATE_OF_BIRTH):
        if type(data[constants.DATE_OF_BIRTH]) != str:
            return None, responses.CODE_INVALID_DATA_TYPE, \
                responses.MESSAGE_INVALID_DATA_TYPE.format(constants.DATE_OF_BIRTH)

        valid_date = common_utils.validate_date_format(date=data[constants.DATE_OF_BIRTH])
        if not valid_date:
            return None, responses.CODE_INVALID_VALUE, \
                responses.MESSAGE_INVALID_VALUE.format(constants.DATE_OF_BIRTH) + ", use format YYYY-MM-DD"

    if data.get(constants.IMAGE):
        if type(data[constants.IMAGE]) != str:
            return None, responses.CODE_INVALID_DATA_TYPE, responses.MESSAGE_INVALID_DATA_TYPE.format(constants.IMAGE)

    user = database_layer.read_single_record(collection=user_model.User,
                                             read_filter={constants.UID: data[constants.UID]})
    if not user:
        return None, responses.CODE_OBJECT_NOT_FOUND, \
            responses.MESSAGE_OBJECT_NOT_FOUND.format(constants.USER, constants.UID)

    if user != token_utils.get_current_user():
        return None, responses.CODE_UNAUTHORIZED_ACCESS, responses.MESSAGE_UNAUTHORIZED_ACCESS

    user_update_data = data
    uid = data[constants.UID]
    user_update_data.pop(constants.UID)
    user_updatable_fields = [constants.NAME, constants.STATUS, constants.GENDER, constants.DATE_OF_BIRTH]
    filtered_user_update_data = common_utils.get_filtered_items(filter_list=user_updatable_fields,
                                                                data=user_update_data)

    if filtered_user_update_data.get(constants.STATUS):
        if filtered_user_update_data[constants.STATUS][constants.ID] != 1:
            token_utils.destroy_user_session_tokens(user=user)

    updated_user = database_layer.modify_records(collection=user_model.User,
                                                 read_filter={constants.UID: uid},
                                                 update_filter=filtered_user_update_data)

    return user_utils.get_user_object(user=updated_user), responses.CODE_SUCCESS, responses.MESSAGE_SUCCESS


def delete_user_controller(uid):
    """
    This function deletes a user based on uid
    :param uid:
    :return:
    """
    if not uid:
        return responses.CODE_MISSING_PARAMETERS, responses.MESSAGE_MISSING_PARAMETERS + ": " + " uid"

    existing_user = database_layer.read_single_record(collection=user_model.User,
                                                      read_filter={constants.UID: uid,
                                                                   constants.STATUS: static_data.user_status[0]})
    if not existing_user:
        return responses.CODE_OBJECT_NOT_FOUND, responses.MESSAGE_OBJECT_NOT_FOUND.format(constants.USER, constants.UID)

    database_layer.delete_record(collection=token_model.Token, delete_filter={constants.USER: existing_user})
    database_layer.delete_record(collection=user_model.User, delete_filter={constants.UID: uid})
    return responses.CODE_SUCCESS, responses.MESSAGE_SUCCESS


def login_user_controller(data):
    """
    This function logins a user based on, email and password, sent inside data
    :param data:
    :return:
    """
    if type(data[constants.PASSWORD]) != str:
        return None, responses.CODE_INVALID_DATA_TYPE, \
            responses.MESSAGE_INVALID_DATA_TYPE.format(constants.PASSWORD)

    if type(data[constants.EMAIL_ADDRESS]) != str:
        return None, None, responses.CODE_INVALID_DATA_TYPE, \
            responses.MESSAGE_INVALID_DATA_TYPE.format(constants.EMAIL_ADDRESS)

    data[constants.EMAIL_ADDRESS] = data[constants.EMAIL_ADDRESS].lower()

    valid_email = common_utils.validate_email_address(email=data[constants.EMAIL_ADDRESS])
    if not valid_email:
        return None, responses.CODE_INVALID_VALUE, responses.MESSAGE_INVALID_VALUE.format(constants.EMAIL_ADDRESS)

    user = database_layer.read_single_record(collection=user_model.User,
                                             read_filter={constants.EMAIL_ADDRESS: data[constants.EMAIL_ADDRESS]})
    if not user:
        return None, None, responses.CODE_INVALID_EMAIL_ADDRESS_OR_PASSWORD, \
            responses.MESSAGE_INVALID_EMAIL_ADDRESS_OR_PASSWORD

    if user[constants.STATUS][constants.ID] == 3:
        return None, None, responses.CODE_USER_IS_SUSPENDED, responses.MESSAGE_USER_IS_SUSPENDED

    if user[constants.STATUS][constants.ID] != 1:
        return None, None, responses.CODE_INVALID_EMAIL_ADDRESS_OR_PASSWORD, \
               responses.MESSAGE_INVALID_EMAIL_ADDRESS_OR_PASSWORD

    if not common_utils.match_password(password=user[constants.PASSWORD],
                                       password_salt=user[constants.PASSWORD_SALT],
                                       user_password=data[constants.PASSWORD]):
        return None, None, responses.CODE_INVALID_EMAIL_ADDRESS_OR_PASSWORD, \
            responses.MESSAGE_INVALID_EMAIL_ADDRESS_OR_PASSWORD

    token_utils.destroy_user_session_tokens(user=user)
    token = token_utils.generate_session_token(user=user)

    return user_utils.get_user_object(user), token, responses.CODE_SUCCESS, responses.MESSAGE_SUCCESS


def logout_user_controller(token):
    """
    This function logs out an authenticated user
    :param token:
    :return:
    """
    token_utils.expire_token(token)
    return responses.CODE_SUCCESS, responses.MESSAGE_SUCCESS


def forgot_password_email(email_address):
    """
    This function will take email address of a user as parameter
    and will generate a token and then will send a verification URL containing id of user and the generated token
    to the email address of a user (this token will be used in reset password API oin case of forgot password)
    :param email_address:
    :return:
    """

    if not common_utils.validate_email_address(email_address):
        return responses.CODE_INVALID_EMAIL_ADDRESS, responses.MESSAGE_INVALID_EMAIL_ADDRESS

    user = database_layer.read_single_record(user_model.User, {constants.EMAIL_ADDRESS: email_address})
    if not user:
        print(f">>>>>>>>>>>>>>>>>>>>>>>>> USER NOT FOUND {email_address}")
        return responses.CODE_INVALID_EMAIL_ADDRESS, responses.MESSAGE_INVALID_EMAIL_ADDRESS

    # BLOCKING FORGOT PASSWORD ON OAUTH SIGN UP
    if user[constants.REGISTRATION_CHANNEL][constants.ID] != 1:
        return responses.CODE_INVALID_CALL, "cannot reset password for user signed up with google, facebook or apple"

    verification_url = token_utils.generate_forgot_password_verification_url(user)
    thread = Thread(target=common_utils.send_mail(), args=("Reset Password Link", user[constants.EMAIL_ADDRESS],
                    "Dear {}, to reset your password, click on the following link: \n{}".format(user.name, verification_url)))
    thread.start()

    return responses.CODE_SUCCESS, responses.MESSAGE_RESET_PASSWORD_EMAIL_SENT


def change_password_by_token(user_id, token, password):
    """
    This function will take id of a user, password he wants to reset and the token which was in the verification URL
    which was sent to the email address (with forgot password API) will reset the password of a user
    using the token
    :param user_id:
    :param token:
    :param password:
    :return:
    """
    user = database_layer.read_single_record(collection=user_model.User,
                                             read_filter={constants.UID: user_id})
    if not user:
        return responses.CODE_OBJECT_NOT_FOUND, responses.MESSAGE_OBJECT_NOT_FOUND.format(constants.USER, constants.UID)

    read_filter = {constants.USER: user, constants.TOKEN: token, 
                   constants.PURPOSE: constants.FORGOT_PASSWORD, constants.IS_EXPIRED: False}

    verification_token = database_layer.read_single_record(token_model.Token, read_filter)

    if not verification_token:
        return responses.CODE_INVALID_TOKEN, responses.MESSAGE_INVALID_TOKEN

    token_utils.expire_token(verification_token)

    if verification_token[constants.EXPIRY_TIME] < common_utils.get_current_time():
        return responses.CODE_TOKEN_EXPIRED, responses.MESSAGE_TOKEN_EXPIRED

    password, password_salt = common_utils.encrypt_password(password)
    update_filter = {constants.PASSWORD: password, constants.PASSWORD_SALT: password_salt}

    database_layer.update_single_record(user_model.User, {constants.UID: user_id}, update_filter)

    return responses.CODE_SUCCESS, responses.MESSAGE_PASSWORD_CHANGED


def change_password(user_id, old_password, new_password):
    """
    This function will take id and old password of a user and a new password which a user wants to set as parameters
    and will match the old password of the user, and then will update the password
    :param user_id:
    :param old_password:
    :param new_password:
    :return:
    """
    user = database_layer.read_single_record(collection=user_model.User,
                                             read_filter={constants.UID: user_id})
    if not user:
        return responses.CODE_OBJECT_NOT_FOUND, responses.MESSAGE_OBJECT_NOT_FOUND.format(constants.USER, constants.UID)

    if user != token_utils.get_current_user():
        return responses.CODE_UNAUTHORIZED_ACCESS, responses.MESSAGE_UNAUTHORIZED_ACCESS

    # BLOCKING CHANGE PASSWORD ON OAUTH SIGN UP
    if user[constants.REGISTRATION_CHANNEL][constants.ID] != 1:
        return responses.CODE_INVALID_CALL, "Cannot change password on social signup"

    if not common_utils.compare_password(user[constants.PASSWORD], old_password):
        return responses.CODE_INVALID_PASSWORD, responses.MESSAGE_PASSWORD_NOT_MATCH

    if old_password == new_password:
        return responses.CODE_INVALID_CALL, "Cannot change to already used password"

    password, password_salt = common_utils.encrypt_password(new_password)
    database_layer.modify_records(user_model.User, {constants.UID: user_id}, {constants.PASSWORD: password,
                                                                              constants.PASSWORD_SALT: password_salt})

    return responses.CODE_SUCCESS, responses.MESSAGE_PASSWORD_CHANGED


def upload_image_controller(_file, _type):
    """
    This function uploads a file to firebase storage bucket and returns url
    :param _file:
    :param _type:
    :return string of url for firebase uploaded image:
    """
    if not _file:
        return None, responses.CODE_MISSING_PARAMETERS, responses.MESSAGE_MISSING_PARAMETERS

    if not _file:
        return None, responses.CODE_MISSING_PARAMETERS, responses.MESSAGE_MISSING_PARAMETERS

    if _type is None:
        _type = 0

    if type(_type) == str and not file_type.isdigit():
        return None, responses.CODE_INVALID_DATA_TYPE, responses.MESSAGE_INVALID_DATA_TYPE.format("file type in url")

    file_type = int(_type)
    if file_type not in [0, 1, 2, 3, 4, 5]:
        return None, responses.CODE_INVALID_CALL, "File type in URL incorrect: should be either 0, 1, 2, 3, 4 or 5"

    file_name = str(uuid.uuid4()) + "_" + datetime.datetime.now().strftime("%Y_%m_%d-%H_%M")
    extension = _file.filename.split('.')[-1]

    if file_type is not None:
        if file_type == 1:
            if extension.lower() not in constants.IMAGE_FORMATS:
                return None, responses.CODE_INVALID_FILE_FORMAT, responses.MESSAGE_INVALID_FILE_FORMAT.format(constants.IMAGE_FORMATS)

        elif file_type == 2:
            if extension.lower() not in [constants.DOCX, constants.PDF]:
                return None, responses.CODE_INVALID_FILE_FORMAT, responses.MESSAGE_INVALID_FILE_FORMAT.format([constants.DOCX, constants.PDF])

        elif file_type == 3:
            if extension.lower() not in constants.MP4:
                return None, responses.CODE_INVALID_FILE_FORMAT, responses.MESSAGE_INVALID_FILE_FORMAT.format(constants.MP4)

        elif file_type == 4:
            if extension.lower() not in constants.MP3:
                return None, responses.CODE_INVALID_FILE_FORMAT, responses.MESSAGE_INVALID_FILE_FORMAT.format(constants.MP3)

        elif file_type == 5:
            if extension.lower() not in constants.EXCEL_FORMATS:
                return None, responses.CODE_INVALID_FILE_FORMAT, responses.MESSAGE_INVALID_FILE_FORMAT.format(constants.EXCEL_FORMATS)

        elif file_type == 0:
            if extension.lower() not in constants.FILE_FORMATS:
                return None, responses.CODE_INVALID_FILE_FORMAT, responses.MESSAGE_INVALID_FILE_FORMAT.format(constants.FILE_FORMATS)

    url = firebase_app.upload_file_using_string(source_file=_file.stream.read(), filename=file_name, extension=extension, content_type=_file.content_type)

    return url, responses.CODE_SUCCESS, responses.MESSAGE_SUCCESS


def social_signup_controller(oauth_code, _type, name=None):
    """
    This function will log in a user through social media accounts
    :param oauth_code:
    :param _type:
    :param name:
    :return:
    """

    if _type not in [constants.FACEBOOK, constants.GOOGLE, constants.APPLE]:
        return None, None, responses.CODE_INVALID_CALL, responses.MESSAGE_INVALID_CALL

    elif _type == constants.GOOGLE:
        response = requests.post(
            url=config.GOOGLE_CONFIG["web"]["token_uri"],
            data={
                "client_id": config.GOOGLE_CONFIG["web"]["client_id"],
                "client_secret": config.GOOGLE_CONFIG["web"]["client_secret"],
                "redirect_uri": (config.GOOGLE_CONFIG["web"]["redirect_uris"][0]),
                "grant_type": "authorization_code",
                "code": oauth_code
            }
        )

        app.logger.error("GOOGLE TOKEN URI RESPONSE: ", str(response.json()))

        if response.status_code != 200:
            return None, None, responses.CODE_INVALID_CALL, responses.MESSAGE_INVALID_CALL

        user_info = user_utils.get_user_info_by_media(response.json()["access_token"], constants.GOOGLE,
                                                      config.GOOGLE_CONFIG["web"]["get_user_info_uri"])

        app.logger.error("GOOGLE USER INFO RESPONSE: ", str(user_info))

        user = database_layer.read_single_record(collection=user_model.User,
                                                 read_filter={constants.EMAIL_ADDRESS: user_info[constants.EMAIL]})

        if user:
            return None, None, responses.CODE_ALREADY_EXISTS, responses.MESSAGE_ALREADY_EXISTS.format(constants.USER, constants.EMAIL_ADDRESS)

        user_data = {
            constants.NAME: user_info[constants.NAME],
            constants.EMAIL_ADDRESS: user_info[constants.EMAIL],
            constants.STATUS: static_data.user_status[0],
            constants.OAUTH_CODE: user_info[constants.ID],
            constants.IMAGE: user_info["picture"],
            constants.REGISTRATION_CHANNEL: static_data.registration_channel[1],
            constants.GENDER: static_data.gender[2]
        }

        new_user = database_layer.insert_record(collection=user_model.User, data=user_data)

        token_utils.destroy_user_session_tokens(new_user)
        token = token_utils.generate_session_token(user=new_user)

        return user_utils.get_user_object(new_user), token, responses.CODE_SUCCESS, responses.MESSAGE_SUCCESS

    elif _type == constants.FACEBOOK:
        response = requests.get(
            config.FACEBOOK_CONFIG["web"]["get_user_info_uri"],
            params={
                "fields": "id, email, name",
                "access_token": oauth_code
            }
        )

        app.logger.error("FACEBOOK RESPONSE: ", str(response.json()))

        if response.status_code != 200:
            return None, None, responses.CODE_INVALID_CALL, responses.MESSAGE_INVALID_CALL

        user_info = response.json()

        user = database_layer.read_single_record(collection=user_model.User,
                                                 read_filter={constants.EMAIL_ADDRESS: user_info[constants.EMAIL]})
        if user:
            return None, None, responses.CODE_ALREADY_EXISTS, responses.MESSAGE_ALREADY_EXISTS.format(constants.USER, constants.EMAIL_ADDRESS)

        if not user_info.get(constants.EMAIL):
            uid = str(uuid.uuid4())
            uid = uid[0:6]
            user_info[constants.EMAIL] = "User-" + uid + "@mail.com"

        user_data = {
            constants.NAME: user_info[constants.NAME],
            constants.EMAIL_ADDRESS: user_info[constants.EMAIL],
            constants.STATUS: static_data.user_status[0],
            constants.OAUTH_CODE: user_info[constants.ID],
            constants.REGISTRATION_CHANNEL: static_data.registration_channel[2],
            constants.GENDER: static_data.gender[2]
        }
        new_user = database_layer.insert_record(collection=user_model.User, data=user_data)

        token_utils.destroy_user_session_tokens(new_user)
        token = token_utils.generate_session_token(user=new_user)

        return user_utils.get_user_object(new_user), token, responses.CODE_SUCCESS, responses.MESSAGE_SUCCESS

    elif _type == constants.APPLE:

        oauth_payload = {
            'iss': config.APPLE_CONFIG["team_id"],
            'iat': round(datetime.now().timestamp()),
            'exp': round(datetime.now().timestamp()) + 15552000,
            'aud': config.APPLE_CONFIG["client_secret_uri"],
            'sub': config.APPLE_CONFIG["client_id"]
        }

        client_secret = jwt.encode(
            oauth_payload,
            config.APPLE_CONFIG["private_key"],
            algorithm='ES256',
            headers={"kid": config.APPLE_CONFIG["key_id"]}
        ).decode("utf-8")

        app.logger.error("GENERATED CLIENT SECRET: ", client_secret)

        config.APPLE_CONFIG["client_secret"] = client_secret

        response = requests.post(
            url=config.APPLE_CONFIG["token_uri"],
            data={
                "client_id": config.APPLE_CONFIG["client_id"],
                "client_secret": config.APPLE_CONFIG["client_secret"],
                "redirect_uri": (config.APPLE_CONFIG["redirect_uris"][0]),
                "grant_type": "authorization_code",
                "code": oauth_code
            },
            headers={'content-type': "application/x-www-form-urlencoded"}
        )

        app.logger.error("APPLE TOKEN URI RESPONSE: " + str(response.json()))

        if response.status_code != 200:
            return None, None, responses.CODE_INVALID_CALL, responses.MESSAGE_INVALID_CALL

        response = response.json()

        id_token = response.get("id_token", None)
        app.logger.error("ID TOKEN FOR APPLE SIGN: : ", id_token)

        user_info = jwt.decode(id_token, '', verify=False)

        app.logger.error("APPLE ID TOKEN USER INFO RESPONSE: " + str(user_info))

        user = database_layer.read_single_record(collection=user_model.User,
                                                 read_filter={constants.EMAIL_ADDRESS: user_info[constants.EMAIL]})
        if user:
            return None, None, responses.CODE_ALREADY_EXISTS, responses.MESSAGE_ALREADY_EXISTS.format(constants.USER, constants.EMAIL_ADDRESS)

        if name is None:
            name = user_info[constants.EMAIL][0:int(user_info[constants.EMAIL].find("@"))]

        user_data = {
            constants.NAME: name,
            constants.EMAIL_ADDRESS: user_info[constants.EMAIL],
            constants.STATUS: static_data.user_state[0],
            constants.OAUTH_CODE: user_info["sub"],
            constants.REGISTRATION_CHANNEL: static_data.registration_channel[3],
            constants.GENDER: static_data.gender[2]
        }
        new_user = database_layer.insert_record(collection=user_model.User, data=user_data)

        token_utils.destroy_user_session_tokens(new_user)
        token = token_utils.generate_session_token(user=new_user)

        return user_utils.get_user_object(new_user), token, responses.CODE_SUCCESS, responses.MESSAGE_SUCCESS


def social_login_controller(oauth_code, _type):
    """
    This function will log in a user based on social media type and oauth code
    :param oauth_code:
    :param _type:
    """

    if _type not in [constants.FACEBOOK, constants.GOOGLE, constants.APPLE]:
        return None, None, responses.CODE_INVALID_CALL, responses.MESSAGE_INVALID_CALL

    elif _type == constants.GOOGLE:
        response = requests.post(
            url=config.GOOGLE_CONFIG["web"]["token_uri"],
            data={
                "client_id": config.GOOGLE_CONFIG["web"]["client_id"],
                "client_secret": config.GOOGLE_CONFIG["web"]["client_secret"],
                "redirect_uri": (config.GOOGLE_CONFIG["web"]["redirect_uris"][0]),
                "grant_type": "authorization_code",
                "code": oauth_code
            }
        )

        app.logger.error("GOOGLE TOKEN URI RESPONSE: ", str(response.json()))

        if response.status_code != 200:
            return None, None, responses.CODE_INVALID_CALL, responses.MESSAGE_INVALID_CALL

        user_info = user_utils.get_user_info_by_media(response.json()["access_token"], _type,
                                                      config.GOOGLE_CONFIG["web"]["get_user_info_uri"])

        app.logger.error("GOOGLE USER INFO URI: ", str(user_info))

        user = database_layer.read_single_record(collection=user_model.User,
                                                 read_filter={
                                                     constants.OAUTH_CODE: user_info[constants.ID],
                                                     constants.REGISTRATION_CHANNEL: static_data.registration_channel[1]
                                                 })

        if not user:
            return None, None, responses.CODE_INVALID_EMAIL_ADDRESS_OR_PASSWORD, responses.MESSAGE_SIGNUP_FIRST.format(constants.GOOGLE)

        if user[constants.STATUS][constants.ID] == 3:
            return None, None, responses.CODE_USER_IS_SUSPENDED, responses.MESSAGE_USER_CANNOT_LOGIN

        if user[constants.STATUS][constants.ID] != 1:
            return user_utils.get_user_object(user), None, responses.CODE_USER_IS_INACTIVE, responses.MESSAGE_USER_IS_INACTIVE

        token_utils.destroy_user_session_tokens(user)
        token = token_utils.generate_session_token(user)

        return user_utils.get_user_object(user), token, responses.CODE_SUCCESS, responses.MESSAGE_SUCCESS

    elif _type == constants.FACEBOOK:
        response = requests.get(
            config.FACEBOOK_CONFIG["web"]["get_user_info_uri"],
            params={
                "fields": "id, email, name",
                "access_token": oauth_code
            }
        )

        if response.status_code != 200:
            return None, None, responses.CODE_INVALID_CALL, responses.MESSAGE_INVALID_CALL

        user_info = response.json()

        app.logger.error("FACEBOOK RESPONSE: ", str(user_info))

        user = database_layer.read_single_record(collection=user_model.User,
                                                 read_filter={
                                                     constants.OAUTH_CODE: user_info[constants.ID],
                                                     constants.REGISTRATION_CHANNEL: static_data.registration_channel[2]
                                                 })

        if not user:
            return None, None, responses.CODE_INVALID_EMAIL_ADDRESS_OR_PASSWORD, responses.MESSAGE_SIGNUP_FIRST.format(constants.FACEBOOK)

        if user[constants.STATUS][constants.ID] == 3:
            return None, None, responses.CODE_USER_IS_SUSPENDED, responses.MESSAGE_USER_CANNOT_LOGIN

        if user[constants.STATUS][constants.ID] != 1:
            return user_utils.get_user_object(user), None, responses.CODE_USER_IS_INACTIVE, responses.MESSAGE_USER_IS_INACTIVE

        token_utils.destroy_user_session_tokens(user)
        token = token_utils.generate_session_token(user)

        return user_utils.get_user_object(user), token, responses.CODE_SUCCESS, responses.MESSAGE_SUCCESS

    elif _type == constants.APPLE:
        oauth_payload = {
            'iss': config.APPLE_CONFIG["team_id"],
            'iat': round(datetime.now().timestamp()),
            'exp': round(datetime.now().timestamp()) + 15552000,
            'aud': config.APPLE_CONFIG["client_secret_uri"],
            'sub': config.APPLE_CONFIG["client_id"],
        }

        client_secret = jwt.encode(
            oauth_payload,
            config.APPLE_CONFIG["private_key"],
            algorithm='ES256',
            headers={"kid": config.APPLE_CONFIG["key_id"]}
        ).decode("utf-8")

        app.logger.error("GENERATED CLIENT SECRET: ", client_secret)

        config.APPLE_CONFIG["client_secret"] = client_secret

        response = requests.post(
            url=config.APPLE_CONFIG["token_uri"],
            data={
                "client_id": config.APPLE_CONFIG["client_id"],
                "client_secret": config.APPLE_CONFIG["client_secret"],
                "redirect_uri": (config.APPLE_CONFIG["redirect_uris"][0]),
                "grant_type": "authorization_code",
                "code": oauth_code
            },
            headers={'content-type': "application/x-www-form-urlencoded"}
        )
        app.logger.error("APPLE TOKEN URI RESPONSE: " + str(response.json()))

        if response.status_code != 200:
            return None, None, None, responses.CODE_INVALID_CALL, responses.MESSAGE_INVALID_CALL

        response = response.json()

        id_token = response.get("id_token", None)
        app.logger.error("ID TOKEN FOR APPLE SIGN: : ", id_token)

        user_info = jwt.decode(id_token, '', verify=False)

        app.logger.error("APPLE ID TOKEN USER INFO RESPONSE: " + str(user_info))

        user = database_layer.read_single_record(collection=user_model.User,
                                                 read_filter={
                                                     constants.OAUTH_CODE: user_info["sub"],
                                                     constants.REGISTRATION_CHANNEL: static_data.registration_channel[3]
                                                 })
        if not user:
            return None, None, responses.CODE_INVALID_EMAIL_ADDRESS_OR_PASSWORD, responses.MESSAGE_SIGNUP_FIRST.format(constants.APPLE)

        if user[constants.STATUS][constants.ID] == 3:
            return None, None, None, responses.CODE_USER_IS_SUSPENDED, responses.MESSAGE_USER_CANNOT_LOGIN

        if user[constants.STATUS][constants.ID] != 1:
            return user_utils.get_user_object(user), None, responses.CODE_USER_IS_INACTIVE, responses.MESSAGE_USER_IS_INACTIVE

        token_utils.destroy_user_session_tokens(user)
        token = token_utils.generate_session_token(user)

        return user_utils.get_user_object(user), token, responses.CODE_SUCCESS, responses.MESSAGE_SUCCESS
