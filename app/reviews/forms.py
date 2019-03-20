##############################################################################################################
# reviews/forms.py
##############################################################################################################

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	body = TextAreaField("Review", validators=[DataRequired()])
	submit = SubmitField("Post")
