import os

class Config():
	DEBUG = True # should be false
	SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI_LOCAL")
	WHOOSH_BASE = "whoosh"
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
	WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY") or "you-will-never-guess"
	MAIL_SERVER = os.environ.get("MAIL_SERVER")
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
	MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


	@staticmethod
	def init_app(app):
		pass

class TestConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI_TEST")
	PRESERVE_CONTEXT_ON_EXCEPTION = False

class ProductionConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = os.environ.get("HEROKU_POSTGRESQL_COBALT_URL")

config = {
    "testing": TestConfig,
    "development": Config,
    "production": ProductionConfig
}
