# Python imports
import uuid

# Framework Imports

# Local imports
from FlaskMongoengineBoilerplate.database.database_initialization import db
from FlaskMongoengineBoilerplate.models.user_model import User
from FlaskMongoengineBoilerplate.utils import common_utils


class Token(db.Document):
    uid = db.StringField(default=str(uuid.uuid4()), unique=True)
    user = db.ReferenceField(User, required=True)
    token = db.StringField(required=True)
    expiry_time = db.IntField(required=True)
    is_expired = db.BooleanField(default=False)
    created_at = db.IntField(default=common_utils.get_current_time())
    updated_at = db.IntField(default=common_utils.get_current_time())

    def __str__(self):
        return f"{self.user.email_address}"
