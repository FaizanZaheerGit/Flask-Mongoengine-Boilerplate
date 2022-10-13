# Python imports

# Framework imports

# Local imports


def get_response_object(response_code, response_data=None, response_message=None):
    """
    This function returns response in form of dict
    :param response_code:
    :param response_data:
    :param response_message:
    :return response_object:
    """
    response_object = {"response_code": response_code}

    if response_data:
        response_object.update({"response_data": response_data})

    if response_message:
        response_object.update({"response_message": response_message})

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
CODE_INVALID_EMAIL_ADDRESS_OR_PASSWORD = 4008


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
MESSAGE_INVALID_EMAIL_ADDRESS_OR_PASSWORD = "Invalid Email Address Or Password"
