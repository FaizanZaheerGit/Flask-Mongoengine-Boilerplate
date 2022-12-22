LOG = "Logs"
LOG_FILE = "FlaskMongoengineBoilerplate.log"
MONGO_DB_HOST = "MONGODB_HOST"
STATUS = "status"
NAME = "name"
ID = "id"
UID = "uid"
EMAIL_ADDRESS = "email_address"
PASSWORD = "password"
PASSWORD_SALT = "password_salt"
GENDER = "gender"
DATE_OF_BIRTH = "date_of_birth"
AGE = "age"
CREATED_AT = "created_at"
UPDATED_AT = "updated_at"
USER = "user"
TOKEN = "token"
EXPIRY_TIME = "expiry_time"
IS_EXPIRED = "is_expired"
IMAGE = "image"

# EXTENSION
XLS = "xls"
XLSX = "xlsx"
CSV = "csv"
PDF = "pdf"
JPG = "jpg"
JPEG = "jpeg"
PNG = "png"
DOCX = "docx"
MP3 = "mp3"
MP4 = "mp4"
IMAGE_FORMATS = [PNG, JPG, JPEG]
EXCEL_FORMATS = [XLS, XLSX, CSV]
MEDICAL_RECORD_FORMAT = [PNG, JPG, JPEG, PDF]
FILE_FORMATS = [PNG, JPG, JPEG, XLS, XLSX, CSV, PDF, DOCX, MP3, MP4]


# FIREBASE
FCM_API_KEY = "FCM_API_KEY"
MAPPERS_EXTENSION = {
    XLS: "application/vnd.ms-excel",
    XLSX: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    CSV: "text/csv",
    JPG: "image/jpeg",
    JPEG: "image/jpeg",
    PDF: "application/pdf",
    PNG: "image/png",
    MP4: "video/mp4",
    MP3: "audio/mpeg",
    DOCX: "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}

EXCEL_CONTENT_TYPES = [MAPPERS_EXTENSION[XLS], MAPPERS_EXTENSION[XLSX], MAPPERS_EXTENSION[CSV]]
IMAGE_CONTENT_TYPES = [MAPPERS_EXTENSION[PNG], MAPPERS_EXTENSION[JPG], MAPPERS_EXTENSION[JPEG]]
DOCUMENT_CONTENT_TYPES = [MAPPERS_EXTENSION[XLS], MAPPERS_EXTENSION[XLSX], MAPPERS_EXTENSION[CSV],
                          MAPPERS_EXTENSION[PNG], MAPPERS_EXTENSION[JPG], MAPPERS_EXTENSION[JPEG],
                          MAPPERS_EXTENSION[MP4], MAPPERS_EXTENSION[MP3], MAPPERS_EXTENSION[DOCX]]
