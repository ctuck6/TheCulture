##############################################################################################################
# articles/forms.py
##############################################################################################################

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from app.models import Company, Article


class ArticleForm(FlaskForm):
	# company = SelectField("Company", choices = [(company.name, company.name) for company in Company.query.all()])
	company = SelectField("Product Company", choices=[("The Company", "The Company"), ("Other", "Other")])
	title = StringField("Title", validators=[DataRequired()])
	body = TextAreaField("Content", validators=[DataRequired()])
	image_file = FileField("Article Picture", validators=[FileAllowed(["jpeg", "png", "jpg"])])
	submit = SubmitField("Post")

	def validate_title(self, title):
		article = Article.query.filter_by(title=title.data.lower()).first()
		if article:
			return False
		return True
