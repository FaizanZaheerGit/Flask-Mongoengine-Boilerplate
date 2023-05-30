# Python imports

# Framework imports

# Local imports


def get_response_object(statusCode, data=None, message=None):
    """
    This function returns response in form of dict
    :param response_code:
    :param response_data:
    :param response_message:
    :return response_object:
    """
    response_object = {"statusCode": statusCode}

    if data:
        response_object.update({"data": data})

    if message:
        response_object.update({"message": message})

    return response_object


# RESPONSE CODES
CODE_SUCCESS = 200
CODE_DEPRECATED_API = 299
CODE_GENERAL_ERROR = 452
CODE_UNAUTHORIZED_ACCESS = 401
CODE_MISSING_PARAMETERS = 4000
CODE_USER_IS_INACTIVE = 4001
CODE_USER_IS_SUSPENDED = 4002
CODE_EXTRA_PARAMETERS = 4003
CODE_OBJECT_NOT_FOUND = 4004
CODE_INVALID_DATA_TYPE = 4005
CODE_INVALID_VALUE = 4006
CODE_ALREADY_EXISTS = 4007
CODE_INVALID_EMAIL_ADDRESS = 4008
CODE_INVALID_EMAIL_ADDRESS_OR_PASSWORD = 4009
CODE_INVALID_CALL = 4010
CODE_INVALID_TOKEN = 4011
CODE_TOKEN_EXPIRED = 4012
CODE_INVALID_PASSWORD = 4013


# RESPONSE MESSAGES
MESSAGE_SUCCESS = "SUCCESS"
MESSAGE_DEPRECATED_API = "API Deprecated"
MESSAGE_GENERAL_ERROR = "Something Went Wrong"
MESSAGE_UNAUTHORIZED_ACCESS = "Unauthorized Access"
MESSAGE_MISSING_PARAMETERS = "Some Parameters Are Missing"
MESSAGE_AUTHENTICATION_FAILED = "Authentication Failed. Invalid Or Expired Token"
MESSAGE_USER_IS_INACTIVE = "User Is Inactive"
MESSAGE_USER_IS_SUSPENDED = "User Is Suspended.\nPLease Contact Support"
MESSAGE_EXTRA_PARAMETERS = "Error: Sending Extra Key"
MESSAGE_OBJECT_NOT_FOUND = "{} With This {} Not Found"
MESSAGE_INVALID_DATA_TYPE = "Invalid Data Type For {}"
MESSAGE_INVALID_VALUE = "Invalid Value For {}"
MESSAGE_INVALID_STATIC_DICT = "{} Value Does Not Match Pre-Built Static Parameters"
MESSAGE_ALREADY_EXISTS = "{} With This {} Already Exists"
MESSAGE_INVALID_EMAIL_ADDRESS = "Invalid Email Address"
MESSAGE_INVALID_EMAIL_ADDRESS_OR_PASSWORD = "Invalid Email Address Or Password"
MESSAGE_INVALID_CALL = "Invalid Call"
MESSAGE_SIGNUP_FIRST = "Please Sign Up with {} first"
MESSAGE_USER_CANNOT_LOGIN = "Cannot Login, Please Contact Support"
MESSAGE_RESET_PASSWORD_EMAIL_SENT = "Password reset e-mail sent successfully"
MESSAGE_INVALID_TOKEN = "Invalid Token"
MESSAGE_TOKEN_EXPIRED = "Token Expired"
MESSAGE_PASSWORD_CHANGED = "Password Changed Successfully"
MESSAGE_PASSWORD_NOT_MATCH = "Passwords do not match"
MESSAGE_INVALID_PAGE_LIMIT = "Error: Make sure to send both page and limit in request query"
