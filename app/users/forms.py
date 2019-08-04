##############################################################################################################
# users/forms.py
##############################################################################################################

from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import current_user
from app.models import Company, User
from app import bcrypt


class AdminForm(FlaskForm):
	search = StringField("Username", validators=[DataRequired()])
	submit = SubmitField("Search")


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
		company = Company.query.filter_by(email=email.data.lower()).first()
		user = User.query.filter_by(email=email.data.lower()).first()
		if company or user:
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


class RoleForm(FlaskForm):
	role = RadioField("Select Role", choices=[("User", "Default User"), ("Administrator", "Administrator")], validators=[DataRequired()])
	save = SubmitField("Save")


class SubscribeForm(FlaskForm):
	email = StringField("Your Email Address", validators=[DataRequired()])
	submit = SubmitField("Subscribe")

	def __init__(self, *args, **kwargs):
		if 'formdata' not in kwargs:
			kwargs['formdata'] = request.args
		if 'csrf_enabled' not in kwargs:
			kwargs['csrf_enabled'] = False
		super(SubscribeForm, self).__init__(*args, **kwargs)


class UpdateAccountForm(FlaskForm):
	firstname = StringField("First name", validators=[DataRequired()])
	lastname = StringField("Last name", validators=[DataRequired()])
	username = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	phone_number = StringField("Phone number", validators=[DataRequired(), Length(min=10, max=20)])
	occupation = StringField("Occupation")
	hometown = StringField("Hometown")
	bio = TextAreaField("Bio")
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


class UpdatePictureForm(FlaskForm):
	image_file = FileField("Choose a file", validators=[FileAllowed(["jpeg", "png", "jpg"])])
	submit = SubmitField("Save Picture")


class UpdatePasswordForm(FlaskForm):
	old_password = PasswordField("Old Password", validators=[DataRequired(), Length(min=4, max=20)])
	new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=4, max=20)])
	confirm_password = PasswordField("Confirm New Password", validators=[DataRequired(), EqualTo("new_password")])
	submit = SubmitField("Change Password")

	def validate_password(self, old_password):
		if bcrypt.check_password_hash(current_user.password, old_password.data):
			return True
		return False
