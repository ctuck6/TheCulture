from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_moment import Moment
from flask_login.login_manager import LoginManager
from flask_mail import Mail
from app.config import config
from flask_wtf.csrf import CSRFProtect
import os

mail = Mail()
database = SQLAlchemy()
moment = Moment()
bcrypt = Bcrypt()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message = "You must be signed in to view that page!"
login_manager.login_message_category = "danger"
login_manager.refresh_view = login_manager.login_view
login_manager.needs_refresh_message = "To protect your account, please re-authenticate to access this page!"
login_manager.needs_refresh_message_category = "danger"


def create_app():
	app = Flask(__name__)
	app.config.from_object(config[os.environ.get("APP_SETTINGS")])

	with app.app_context():
		database.init_app(app)
		bcrypt.init_app(app)
		login_manager.init_app(app)
		mail.init_app(app)
		csrf.init_app(app)
		moment.init_app(app)

	from app.users.routes import users
	from app.articles.routes import articles
	from app.reviews.routes import reviews
	from app.comments.routes import comments
	from app.likes.routes import likes
	from app.main.routes import main
	from app.errors.handlers import errors
	from app.products.routes import products
	from app.companies.routes import companies
	app.register_blueprint(users)
	app.register_blueprint(articles)
	app.register_blueprint(reviews)
	app.register_blueprint(comments)
	app.register_blueprint(likes)
	app.register_blueprint(main)
	app.register_blueprint(errors)
	app.register_blueprint(products)
	app.register_blueprint(companies)

	return app
