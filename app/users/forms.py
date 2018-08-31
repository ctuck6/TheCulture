from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.database import User

class RegistrationForm(FlaskForm):
	username = StringField("Username", validators = [DataRequired(), Length(min = 4, max = 20)])
	email = StringField("Email", validators = [DataRequired(), Email()])
	password = PasswordField("Password", validators = [DataRequired()])
	confirmPassword = PasswordField("Re-Enter Password", validators = [DataRequired(), EqualTo("password")])
	submit = SubmitField("Sign Up")

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user:
			raise ValidationError("Username already exists. Please try again.")

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError("Email already exists. Please try again.")

class LoginForm(FlaskForm):
	email = StringField("Email", validators = [DataRequired(), Email()])
	password = PasswordField("Password", validators = [DataRequired()])
	remember = BooleanField("Remember Me")
	submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
	username = StringField("Username", validators = [DataRequired(), Length(min = 4, max = 20)])
	email = StringField("Email", validators = [DataRequired(), Email()])
	profilePicture = FileField("Update Profile Picture", validators = [FileAllowed(["jpeg", "png", "jpg"])])
	submit = SubmitField("Save Changes")

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username = username.data).first()
			if user:
				raise ValidationError("Username already exists. Please try again.")

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email = email.data).first()
			if user:
				raise ValidationError("Email already exists. Please try again.")

class RequestResetForm(FlaskForm):
	email = StringField("Email", validators = [DataRequired(), Email()])
	submit = SubmitField("Request Password Reset")

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if not user:
			raise ValidationError("Email does not exists. Please try again.")

class ResetPasswordForm(FlaskForm):
	password = PasswordField("Password", validators = [DataRequired()])
	confirmPassword = PasswordField("Re-Enter Password", validators = [DataRequired(), EqualTo("password")])
	submit = SubmitField("Reset Password")