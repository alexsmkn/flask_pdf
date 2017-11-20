import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Settings:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '123qwe123'
    SQLALCHEMY_DATABASE_URI = "postgresql://flask_pdf:123qwe@localhost:5432/flask_pdf"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
