##############################################################################################################
# products/routes.py
##############################################################################################################

from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from app import database
from app.models import Review, Product, Company, Permission
from app.products.forms import ProductForm, FilterForm
from app.reviews.forms import ReviewForm
from app.decorators import permission_required
from app.constants import Constants

products = Blueprint("products", __name__)

@products.route("/product/<int:product_id>/delete", methods=["GET", "POST"])
@login_required
@permission_required(Permission.MANAGE_PRODUCTS)
def delete_product(product_id):
	product = Product.query.get_or_404(product_id)
	if product.company != current_user:
		abort(Constants.FORBIDDEN_PAGE_ERROR_PAGE)
	database.session.delete(product)
	database.session.commit()
	flash("Your product has been deleted!", "success")
	return redirect(url_for("products.show_products", product_id=product_id))

@products.route("/product/new", methods=["GET", "POST"])
@login_required
@permission_required(Permission.MANAGE_PRODUCTS)
def new_product():
	form = ProductForm()
	form.company.choices = [("Other", "Other")] + [(company.name, company.name) for company in Company.query.all()]
	if form.validate_on_submit():
		if not form.validate_name(form.name):
			flash("Product name already being used. Please try again", "danger")
		else:
			company = Company.query.filter_by(name=form.company.data).first()
			product = Product(name=form.name.data,
							company=company,
							price=form.price.data,
							description=form.description.data,
							image_file=form.image_file.data)
			database.session.add(product)
			database.session.commit()
			flash("Your product has been posted!", "success")
			product = Product.query.filter_by(name=form.name.data).first_or_404()
			return redirect(url_for("products.product", product_id=product.id))
	return render_template("new_product.html", legend="New Product", form=form)

@products.route("/product/<int:product_id>", methods=["GET", "POST"])
def product(product_id):
	product = Product.query.get_or_404(product_id)
	reviews = product.reviews.all()
	if len(reviews) > 0:
		rating = int(round(sum([review.rating for review in reviews])/len(reviews)))
	else:
		rating = 0
	form = ReviewForm()
	if form.validate_on_submit():
		if current_user.is_authenticated:
			review = Review(title=form.title.data,
							rating=form.rating.data,
							body=form.body.data,
							reviewer=current_user._get_current_object(),
							product=product)
			database.session.add(review)
			database.session.commit()
			flash("Your review has been posted!", "success")
			return redirect(url_for('products.product', product_id=product_id))
		else:
			flash("You must be logged in to leave a review!", "danger")
			abort(Constants.FORBIDDEN_PAGE_ERROR_PAGE)
	return render_template("product.html", product=product, reviews=reviews, form=form, rating=rating)

@products.route("/products", methods=["GET", "POST"])
def show_products():
	form = FilterForm()
	page = request.args.get("page", 1, type=int)
	if form.validate_on_submit():
		if form.filter_choice.data == "price":
			products = Product.query.order_by(Product.price).paginate(page=page, per_page=Constants.PRODUCTS_ON_SHOW_PRODUCTS_PAGE)
		if form.filter_choice.data == "date_posted":
			products = Product.query.order_by(Product.date_posted).paginate(page=page, per_page=Constants.PRODUCTS_ON_SHOW_PRODUCTS_PAGE)
		if form.filter_choice.data == "rating":
			products = Product.query.order_by(Product.rating).paginate(page=page, per_page=Constants.PRODUCTS_ON_SHOW_PRODUCTS_PAGE)
	else:
		products = Product.query.paginate(page=page, per_page=Constants.PRODUCTS_ON_SHOW_PRODUCTS_PAGE)
	prev_page = url_for('products.show_products', page=products.prev_num)
	next_page = url_for('products.show_products', page=products.next_num)
	return render_template("show_products.html", paginate=True, prev_page=prev_page, next_page=next_page, form=form, products=products)

@products.route("/product/<int:product_id>/update",  methods=["GET", "POST"])
@login_required
@permission_required(Permission.MANAGE_PRODUCTS)
def update_product(product_id):
	product = Product.query.get_or_404(product_id)
	form = ProductForm()
	valid_input = True
	if product.company != current_user:
		abort(Constants.FORBIDDEN_PAGE_ERROR_PAGE)
	if form.validate_on_submit():
		if form.validate_name(form.name):
			product.name = form.name.data
		else:
			valid_input = False
			flash("Username already being used. Please try again", "danger")
		if form.company.data and form.company.data != product.company.name:
			product.company = Company.query.filter_by(name=form.company.data).first()
		if form.price.data and form.price.data != product.price:
			product.price = form.price.data
		if form.description.data and form.description.data != product.description:
			product.description = form.description.data
		if form.image_file.data and form.image_file.data != product.image_file:
			product.image_file = form.image_file.data
		if valid_input:
			database.session.commit()
			flash("Your product has been updated!", "success")
		return redirect(url_for("products.product", product_id=product.id))
	elif request.method == "GET":
		form.name.data = product.name
		if product.company:
			form.company.data = product.company.name
		form.price.data = product.price
		form.description.data = product.description
	return render_template("new_product.html", legend="Update Product", form=form)
