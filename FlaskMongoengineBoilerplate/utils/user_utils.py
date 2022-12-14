# Python imports
from datetime import datetime

# Framework imports
from flask_mongoengine import BaseQuerySet

# Local imports
from FlaskMongoengineBoilerplate.utils import constants


def user_age_calculator(date_of_birth):
    """
    returns Age according to date_of_birth
    :param date_of_birth:
    :return age based on date_of_birth:
    """
    today = datetime.now()
    birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def get_user_object(user):
    """
    returns specific information about user
    :param user:
    :return an object of a user:
    """
    user_data = {
        constants.UID: user[constants.UID],
        constants.NAME: user[constants.NAME],
        constants.EMAIL_ADDRESS: user[constants.EMAIL_ADDRESS],
        constants.STATUS: user[constants.STATUS],
        constants.GENDER: user[constants.GENDER],
        constants.DATE_OF_BIRTH: user[constants.DATE_OF_BIRTH],
        constants.AGE: user_age_calculator(user[constants.DATE_OF_BIRTH])
        if user[constants.DATE_OF_BIRTH] else ""
    }
    return user_data


def filter_user_object(users):
    """
    This function takes a list of all users as a parameter
    and returns information about all users, as a list
    :param users:
    :return get user object of multiple users:
    """
    if isinstance(users, BaseQuerySet) or isinstance(users, list):
        user_data = []
        for user in users:
            user_data.append(get_user_object(user))
        return user_data

    return [get_user_object(users)]
