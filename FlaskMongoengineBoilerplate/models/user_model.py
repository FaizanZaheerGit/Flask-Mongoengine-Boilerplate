# Python imports

# Framework Imports

# Local imports
from FlaskMongoengineBoilerplate.database.database_initialization import db
from FlaskMongoengineBoilerplate.config import static_data
from FlaskMongoengineBoilerplate.utils import common_utils


class User(db.Document):
    oauth_code = db.StringField(default="")
    name = db.StringField(required=True)
    email_address = db.EmailField(required=True)
    password = db.StringField(required=True)
    image = db.StringField(default="")
    gender = db.DictField(required=True)
    date_of_birth = db.StringField(default="")
    registration_channel = db.DictField(default=static_data.registration_channel[0])
    status = db.DictField(default=static_data.user_status[0])
    created_at = db.IntField(default=common_utils.get_current_time())
    updated_at = db.IntField(default=common_utils.get_current_time())

    def __str__(self):
        return f"{self.email_address}"
