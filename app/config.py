import os
from whoosh.analysis import StemmingAnalyzer

class Config():
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI_DEVELOPMENT")
	WHOOSH_BASE = "whoosh"
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
	WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY") or "you-will-never-guess"
	MAIL_SERVER = os.environ.get("MAIL_SERVER")
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
	MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
	SESSION_COOKIE_SECURE = False
	WHOOSH_ANALYZER = StemmingAnalyzer()
	TESTING = False
	THECULTURE_ADMIN = os.environ.get("THECULTURE_ADMIN")


class TestConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI_TEST")
	PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
	TESTING = False
	MAINTENANCE_MODE = False
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = os.environ.get("HEROKU_POSTGRESQL_COBALT_URL")

config = {
    "test": TestConfig,
    "development": Config,
    "production": ProductionConfig
}
