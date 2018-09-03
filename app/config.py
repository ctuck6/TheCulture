import os

class Config():
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.environ.get("SECRET_KEY")
	MAIL_SERVER = os.environ.get("MAIL_SERVER")
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
	MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")