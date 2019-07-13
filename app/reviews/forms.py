##############################################################################################################
# reviews/forms.py
##############################################################################################################

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, SelectField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
	title = StringField("Title *", validators=[DataRequired()])
	rating = SelectField("Your rating *", coerce=int, choices=[(5, "(5/5)"), (4, "(4/5)"), (3, "(3/5)"), (2, "(2/5)"), (1, "(1/5)")], validators=[DataRequired()])
	body = TextAreaField("Review body *", validators=[DataRequired()])
	submit = SubmitField("Post Review")
