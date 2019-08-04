##############################################################################################################
# reviews/routes.py
##############################################################################################################

from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required
from app import database
from app.models import Review, Product, Permission
from app.decorators import permission_required
from app.constants import Constants

reviews = Blueprint("reviews", __name__)


@reviews.route("/review/<int:product_id>/<int:review_id>/delete",  methods=["GET", "POST"])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def delete_review(product_id, review_id):
	review = Review.query.get_or_404(review_id)
	if review.author != current_user:
		abort(Constants.FORBIDDEN_PAGE_ERROR_PAGE)
	database.session.delete(review)
	database.session.commit()
	flash("Your post has been deleted!", "success")
	return redirect(url_for("products.product", product_id=product_id))


@reviews.route("/review/save", methods=["GET", "POST"])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def save_review():
	product = Product.query.get_or_404(request.form.get('product_id'))
	review = Review.query.get_or_404(request.form.get('review_id'))
	review.body = request.form.get('body')
	database.session.commit()
	return render_template("jquery/review.html", review=review, product=product)


@reviews.route("/review/update", methods=["POST"])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def update_review():
	product = Product.query.get_or_404(request.form.get('product_id'))
	review = Review.query.get_or_404(request.form.get('review_id'))
	return render_template("jquery/review_form.html", review=review, product=product)
