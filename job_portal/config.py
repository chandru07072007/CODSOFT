from os import environ

class Config:
    SECRET_KEY = environ.get('3a6e84a3c1229d70f4d5644dd2a2d27a9b725d8a6045a1f09bb4eb579c13b22d')
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'chandrupalanisamyaids@gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'chandrupalanisamyaids@gmail.com'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit upload size to 16 MB
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}