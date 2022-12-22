# Python imports
import firebase_admin
from firebase_admin import storage, messaging

# Framework imports

# Local imports
from FlaskMongoengineBoilerplate.config import config
from FlaskMongoengineBoilerplate.utils import constants


class FirebaseUtils:
    app = None
    storage_bucket = None
    credentials = config.FIREBASE_CONFIG

    def __init__(self):
        self.initialize_app()
        self.initialize_bucket()

    def initialize_app(self):
        cred = firebase_admin.credentials.Certificate(self.credentials)
        self.app = firebase_admin.initialize_app(cred)

    def initialize_bucket(self):
        self.storage_bucket = storage.bucket(name=self.credentials["StorageBucket"], app=self.app)

    def download_file(self, source_file_path, destination_file_path):
        blob = self.storage_bucket.blob(source_file_path)
        blob.download_to_filename(destination_file_path)

    def upload_file(self, source_file_path, filename, extension, image=False, report=False, file=False):
        blob = None
        if image:
            blob = self.storage_bucket.blob(f"images/{filename}.{extension}")
        elif report:
            blob = self.storage_bucket.blob(f"reports/{filename}.{extension}")
        elif file:
            blob = self.storage_bucket.blob(f"files/{filename}.{extension}")

        blob.upload_from_filename(source_file_path)
        blob.make_public()
        return blob.public_url

    def upload_file_using_string(self, source_file, filename, extension, content_type=None):
        """
        This function is responsible to upload data to firebase ie images, pdf and any sort of other documents
        :param source_file:
        :param filename:
        :param extension:
        :param content_type:
        :return:
        """

        if content_type in constants.EXCEL_CONTENT_TYPES:
            blob = self.storage_bucket.blob(f"files/{filename}.{extension}")
            blob.upload_from_string(source_file, content_type=content_type)
            blob.make_public()
            return blob.public_url

        elif content_type in constants.MAPPERS_EXTENSION[constants.PDF]:
            blob = self.storage_bucket.blob(f"reports/{filename}.{extension}")
            blob.upload_from_string(source_file, content_type=content_type)
            blob.make_public()
            return blob.public_url

        elif content_type in constants.IMAGE_CONTENT_TYPES:
            blob = self.storage_bucket.blob(f"images/{filename}.{extension}")
            blob.upload_from_string(source_file, content_type=content_type)
            blob.make_public()
            return blob.public_url

        elif content_type in constants.DOCUMENT_CONTENT_TYPES:
            print(content_type)
            blob = self.storage_bucket.blob(f"other/{filename}.{extension}")
            blob.upload_from_string(source_file, content_type=content_type)
            blob.make_public()
            return blob.public_url

        return None

    def delete_file(self, filename, extension, content_type=None):
        """
        This function is responsible to remove data on firebase ie images, pdf and any sort of other documents
        :param filename:
        :param extension:
        :param content_type:
        :return:
        """

        if content_type in constants.EXCEL_CONTENT_TYPES:
            blob = self.storage_bucket.blob(f"files/{filename}.{extension}")
            if blob.exists():
                blob.delete()
            return True

        elif content_type in constants.MAPPERS_EXTENSION[constants.PDF]:
            blob = self.storage_bucket.blob(f"reports/{filename}.{extension}")
            if blob.exists():
                blob.delete()
            return True

        elif content_type in constants.IMAGE_CONTENT_TYPES:
            blob = self.storage_bucket.blob(f"images/{filename}.{extension}")
            if blob.exists():
                blob.delete()
            return True

        elif content_type in constants.DOCUMENT_CONTENT_TYPES:
            blob = self.storage_bucket.blob(f"other/{filename}.{extension}")
            if blob.exists():
                blob.delete()
            return True

        return False

    def delete_app(self):
        firebase_admin.delete_app(self.app)

    def get_notification_icon(self):
        """
        This function returns public url of notification image
        (stored with the name appstore.png) in firebase storage
        :return:
        """
        blob = self.storage_bucket.blob(f"images/notification_icon.png")
        blob.make_public()
        return blob.public_url
