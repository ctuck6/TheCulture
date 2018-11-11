from flask import Flask, render_template, flash, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import config
from sqlalchemy_searchable import make_searchable
import flask_whooshalchemyplus, os
from flask_wtf.csrf import CSRFProtect

mail = Mail()
database = SQLAlchemy()
make_searchable(database.metadata)
bcrypt = Bcrypt()
csrf = CSRFProtect()
loginManager = LoginManager()
loginManager.login_view = "users.login"
loginManager.login_message = "You must be signed in to view that page!"
loginManager.login_message_category = "danger"


def create_app(config_class):
	app = Flask(__name__)
	app.config.from_object(config[os.environ["APP_SETTINGS"]])

	with app.app_context():
		database.init_app(app)
		bcrypt.init_app(app)
		loginManager.init_app(app)
		mail.init_app(app)
		flask_whooshalchemyplus.init_app(app)
		csrf.init_app(app)

	from app.users.routes import users
	from app.reviews.routes import reviews
	from app.main.routes import main
	from app.errors.handlers import errors
	app.register_blueprint(users)
	app.register_blueprint(reviews)
	app.register_blueprint(main)
	app.register_blueprint(errors)

	return app
