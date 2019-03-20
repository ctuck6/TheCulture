##############################################################################################################
# users/forms.py
##############################################################################################################

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User


class AdminForm(FlaskForm):
	role = RadioField("Select Role", choices=[("User", "Default User"), ("Administrator", "Administrator")], validators=[DataRequired()])
	save = SubmitField("Save")


class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	remember = BooleanField("Remember Me")
	submit = SubmitField("Login")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data.lower()).first()
		if user:
			return True
		return False


class RegistrationForm(FlaskForm):
	firstname = StringField("First name", validators=[DataRequired(), Length(min=2, max=20)])
	lastname = StringField("Last name", validators=[DataRequired(), Length(min=2, max=20)])
	username = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=20)])
	confirm_password = PasswordField("Re-Enter Password", validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Sign Up")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data.lower()).first()
		if user:
			return False
		return True

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data.lower()).first()
		if user:
			return False
		return True

	def validate_phone_number(self, phone_number):
		user = User.query.filter_by(phone_number=phone_number.data).first()
		if user:
			return False
		return True


class ResetPasswordForm(FlaskForm):
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Re-Enter Password", validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Reset Password")


class RequestResetForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	submit = SubmitField("Reset Password")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data.lower()).first()
		if not user:
			return False
		return True


class UpdateAccountForm(FlaskForm):
	firstname = StringField("First name", validators=[DataRequired()])
	lastname = StringField("Last name", validators=[DataRequired()])
	username = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	phone_number = StringField("Phone number", validators=[DataRequired(), Length(min=10, max=10)])
	occupation = StringField("Occupation")
	bio = TextAreaField("Bio")
	image_file = FileField("Update Profile Picture", validators=[FileAllowed(["jpeg", "png", "jpg"])])
	submit = SubmitField("Save Changes")

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data.lower()).first()
			if user:
				return False
		return True

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data.lower()).first()
			if user:
				return False
		return True

	def validate_phone_number(self, phone_number):
		if phone_number.data != current_user.phone_number:
			user = User.query.filter_by(phone_number=phone_number.data).first()
			if user:
				return False
		return True
