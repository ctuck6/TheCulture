##############################################################################################################
# comments/forms.py
##############################################################################################################

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
	body = TextAreaField("Post a comment", validators=[DataRequired()])
	submit = SubmitField("Comment")
