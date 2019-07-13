from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import Company, User
from us import states
from pycountry import countries


class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	remember = BooleanField("Remember Me")
	submit = SubmitField("Login")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data.lower()).first()
		if not user:
			user = Company.query.filter_by(email=email.data.lower()).first()
		if user:
			return True
		return False


class RegistrationForm(FlaskForm):
	name = StringField("Company name", validators=[DataRequired(), Length(max=50)])
	address = StringField("Address", validators=[DataRequired()])
	city = StringField("City", validators=[DataRequired()])
	state = SelectField("State", choices=[(None, "None")] + [(state.name, state.name) for state in states.STATES], default=None)
	zip_code = StringField("Zip code", validators=[DataRequired(), Length(min=5, max=10)])
	country = SelectField("Country", choices=[("Other", "Other")] + [(country.name, country.name) for country in countries], default="Other")
	phone_number = StringField("Phone number", validators=[DataRequired(), Length(min=10, max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	website = StringField("Website", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Re-Enter Password", validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Register")


	def validate_email(self, email):
		company = Company.query.filter_by(email=email.data.lower()).first()
		user = User.query.filter_by(email=email.data.lower()).first()
		if company or user:
			return False
		return True

	def validate_address(self, address):
		company = Company.query.filter_by(address=address.data.lower()).first()
		if company:
			return False
		return True

	def validate_phone_number(self, phone_number):
		company = Company.query.filter_by(phone_number=phone_number.data).first()
		if company:
			return False
		return True

	def validate_website(self, website):
		company = Company.query.filter_by(website=website.data.lower()).first()
		if company:
			return False
		return True
