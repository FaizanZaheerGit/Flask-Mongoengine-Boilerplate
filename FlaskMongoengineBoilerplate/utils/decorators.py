# Python imports

# Local imports
from FlaskMongoengineBoilerplate import app
from FlaskMongoengineBoilerplate.utils import common_utils, responses, constants, token_utils

# Framework imports
from functools import wraps
from flask import jsonify, request


def validator(required_fields=[], optional_fields=[]):
    def decorator(view_function):

        @wraps(view_function)
        def wrapper(*args, **kwargs):

            if not required_fields:
                return view_function(*args, **kwargs)

            data = common_utils.get_posted_data()
            validated_data = {}
            if type(data) != dict:
                response_obj = responses.get_response_object(response_code=responses.CODE_MISSING_PARAMETERS,
                                                             response_message="Data sent is not a valid JSON object!")
                app.logger.error(f" {request.method} {request.url} \nHeaders: {dict(request.headers)} \n"
                                 f"Body: {data}", exc_info=1)
                return jsonify(response_obj)

            combined_list = required_fields + optional_fields
            missing_list = []
            for key in data.keys():
                if key not in combined_list:
                    response_obj = responses.get_response_object(response_code=responses.CODE_EXTRA_PARAMETERS,
                                                                 response_message=responses.MESSAGE_EXTRA_PARAMETERS
                                                                 + ": " + key)
                    app.logger.error(f" {request.method} {request.url} \nHeaders: {dict(request.headers)} \n"
                                     f"Body: {data}", exc_info=1)
                    return jsonify(response_obj)

                if key in required_fields:
                    if data.get(key) in [None, ""]:
                        missing_list.append(key)
                    else:
                        validated_data.update({key: data[key]})
                elif key not in required_fields:
                    if key in optional_fields:
                        validated_data.update({key: data[key]})

            for field in required_fields:
                if field not in validated_data.keys():
                    missing_list.append(field)

            data = validated_data
            if missing_list:
                response_obj = responses.get_response_object(response_code=responses.CODE_MISSING_PARAMETERS,
                                                             response_message=responses.MESSAGE_MISSING_PARAMETERS
                                                             + ": " + str(missing_list))
                app.logger.error(f" {request.method} {request.url} \nHeaders: {dict(request.headers)} \n"
                                 f"Body: {common_utils.get_posted_data()}", exc_info=1)
                return jsonify(response_obj)

            return view_function(data, *args, **kwargs)

        return wrapper

    return decorator


def is_authenticated(view_function):
    @wraps(view_function)
    def decorator(*args, **kwargs):

        user = token_utils.check_current_user()
        if not user:
            response = responses.get_response_object(response_code=responses.CODE_UNAUTHORIZED_ACCESS,
                                                     response_message=responses.MESSAGE_AUTHENTICATION_FAILED)
            return jsonify(response)

        if user[constants.STATUS][constants.ID] != 1:
            # DESTROY USER SESSION TOKEN
            token_utils.destroy_user_session_tokens(user)
            response = responses.get_response_object(response_code=responses.CODE_USER_IS_INACTIVE,
                                                     response_message=responses.MESSAGE_USER_IS_INACTIVE)
            return jsonify(response)

        return view_function(*args, **kwargs)

    return decorator


def logging(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):

        try:
            response = view_function(*args, **kwargs)
            return response

        except Exception as e:
            print(str(e))
            app.logger.error(f" {request.method} {request.url} \nHeaders: {dict(request.headers)} \n"
                             f"Body: {common_utils.get_posted_data()}", exc_info=1)

            response = responses.get_response_object(response_code=responses.CODE_GENERAL_ERROR,
                                                     response_message=responses.MESSAGE_GENERAL_ERROR)
            return jsonify(response)

    return wrapper


def blocked(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        print("Args: ", args, "\nKwargs: ", kwargs)
        response = responses.get_response_object(response_code=responses.CODE_DEPRECATED_API,
                                                 response_message=responses.MESSAGE_DEPRECATED_API)
        return jsonify(response)

    return wrapper
