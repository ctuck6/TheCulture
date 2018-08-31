from flask import Flask, render_template, flash, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
loginManager = LoginManager()
loginManager.login_view = "users.login"
loginManager.login_message_category = "danger"

def create_app(config_class = Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	mail.init_app(app)
	db.init_app(app)
	bcrypt.init_app(app)
	loginManager.init_app(app)

	from app.users.routes import users
	from app.main.routes import main
	from app.reviews.routes import reviews
	from app.errors.handlers import errors
	app.register_blueprint(users)
	app.register_blueprint(main)
	app.register_blueprint(reviews)
	app.register_blueprint(errors)

	return app