import os

class Config():
	DEBUG = True # should be false
	SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI_LOCAL"]
	WHOOSH_BASE = "whoose"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.environ["SECRET_KEY"] or "you-will-never-guess"
	WTF_CSRF_SECRET_KEY = os.environ["WTF_CSRF_SECRET_KEY"] or "you-will-never-guess"
	MAIL_SERVER = os.environ["MAIL_SERVER"]
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ["MAIL_USERNAME"]
	MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]


	@staticmethod
	def init_app(app):
		pass

class TestConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI_TEST"]
	PRESERVE_CONTEXT_ON_EXCEPTION = False

class ProductionConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = os.environ["HEROKU_POSTGRESQL_COBALT_URL"]

config = {
    "testing": TestConfig,
    "default": Config,
    "production": ProductionConfig
}
