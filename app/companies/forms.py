from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User
from app.utils import us_states, countries


class RegistrationForm(FlaskForm):
	name = StringField("Company name", validators=[DataRequired(), Length(max=50)])
	address = StringField("Address", validators=[DataRequired(), Length(max=100)])
	city = StringField("City", validators=[DataRequired(), Length(max=30)])
	state = SelectField("State", choices=sorted([(state, state) for abbr, state in us_states.iteritems()]))
	zip_code = StringField("Zip code", validators=[DataRequired(), Length(min=5, max=10)])
	country = SelectField("Country", choices=sorted([(country, country) for abbr, country in countries.iteritems()]))
	phone_number = StringField("Phone number", validators=[DataRequired(), Length(min=10, max=10)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Re-Enter Password", validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Register")


	def validate_email(self, email):
		user = User.query.filter_by(email=email.data.lower()).first()
		if user:
			return False
		return True

	def validate_address(self, address):
		user = User.query.filter_by(address=address.data.lower()).first()
		if user:
			return False
		return True

	def validate_phone_number(self, phone_number):
		user = User.query.filter_by(phone_number=phone_number.data).first()
		if user:
			return False
		return True
