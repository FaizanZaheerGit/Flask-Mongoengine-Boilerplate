# Python Imports
import time
import datetime
import re

# Framework Imports
from flask import request
from flask_scrypt import generate_random_salt, generate_password_hash, check_password_hash
from flask_mail import Message

# Local Imports
from FlaskMongoengineBoilerplate.config import config
from FlaskMongoengineBoilerplate import app, mail


def get_current_time(hours=0, days=0):
    """
    This Function Returns Serialized Time in Epoch According To Given hours, and days
    :param hours:
    :param days:
    :return current time in epoch:
    """
    return int(time.mktime(
        (datetime.datetime.utcnow() + datetime.timedelta(hours=hours, days=days)).timetuple()))


def get_posted_data(method="POST"):
    """
    This Function Returns data posted by user in API request depending on method (GET, POST, etc.)
    :param method:
    :return posted request data in accordance with method:
    """
    if method.upper() == "GET":
        return request.args

    elif method.upper() == "FORM":
        return request.form

    else:
        return request.get_json(silent=True) or {}


def get_posted_files():
    """
    This function returns posted files in form data
    :param:
    :return Posted files in Form Data:
    """
    return request.files


def validate_email_address(email):
    """
    validates email address
    :param: email
    """
    if email is not None:
        # check that email is not starting with a character, has @ and . in appropriate positions
        if re.match(r'^(?![.%+-])[a-zA-Z0-9._%+-]+[a-zA-Z0-9]+@[a-zA-Z0-9]+[+-]{0,1}[a-zA-Z0-9]+\.'
                    r'[a-zA-Z]+\.{0,1}[a-zA-Z]+$', email):
            return True

    return False


def validate_date_format(date):
    """
    This function checks whether the entered date is in correct format
    :param date:
    :return:
    """
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def convert_string_to_bytes(line):
    """
    converts string to bytes
    :param line:
    :return:
    """
    return str.encode(line)


def convert_byte_to_string(byte_str):
    """
    converts bytes to string
    :param byte_str:
    :return:
    """
    return byte_str.decode("utf-8")


def match_password(password, password_salt, user_password):
    """
    checks whether the user password is same as given password
    :param password:
    :param password_salt:
    :param user_password:
    :return:
    """
    return convert_string_to_bytes(password) == \
        generate_password_hash(
            user_password, convert_string_to_bytes(password_salt))


def encrypt_password(user_password):
    """
    This function encrypts the password entered by user using random generated salt and returns the encrypted password
    hash and salt
    :param user_password:
    :return:
    """
    password_salt = generate_random_salt()

    return convert_byte_to_string(generate_password_hash(user_password, password_salt)), \
        convert_byte_to_string(password_salt)


def compare_password(password, user_password):
    """
    Checks if two passwords are the same or not
    :param password:
    :param user_password:
    :return:
    """
    return check_password_hash(password, user_password)


def send_mail(subject, recipients, body, html=None):
    """
    This function sends an e-mail to an email_address
    :param subject:
    :param recipients:
    :param body:
    :param html:
    :return :
    """
    with app.app_context():
        msg = Message(subject=subject,
                      sender=("TEST EMAIL USER", config.EMAIL_USER),
                      recipients=[recipients],
                      body=body)
        if html:
            msg.html = html
        mail.send(msg)


def get_filtered_items(filter_list, data):
    """
    This function takes a list of filter items, and extracts the items from the data dict
    :param filter_list:
    :param data:
    :return:
    """
    filtered_data = {}
    for item in filter_list:
        if item in dict(data).keys():
            filtered_data.update({item: data[item]})
    return filtered_data
