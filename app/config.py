import os

class Config():
	DEBUG = True # should be false
	SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
	WHOOSH_BASE = "whoose"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.environ.get("SECRET_KEY")
	WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY")
	MAIL_SERVER = os.environ.get("MAIL_SERVER")
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
	MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
	SERVER_NAME = "gunicorn/19.9.0"

class TestConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
