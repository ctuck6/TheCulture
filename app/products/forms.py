##############################################################################################################
# products/forms.py
##############################################################################################################

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired
from app.models import Product


class ProductForm(FlaskForm):
	company = SelectField("Product Company")
	name = StringField("Product Name", validators=[DataRequired()])
	price = StringField('Product Price', validators=[DataRequired()])
	description = TextAreaField("Product Description", validators=[DataRequired()])
	image_file = FileField("Product Picture", validators=[FileAllowed(["jpeg", "png", "jpg"])])
	submit = SubmitField("Submit")

	def validate_name(self, name):
		product = Product.query.filter_by(name=name.data.lower()).first()
		if product:
			return False
		return True


class FilterForm(FlaskForm):
	filter_choice = SelectField(choices=[("price", "Price"), ("rating", "Rating"), ("date_posted", "Newest First")])
