##############################################################################################################
# reviews/routes.py
##############################################################################################################


from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user, login_required
from app import database
from app.models import Review, Product, Permission
from app.reviews.forms import ReviewForm
from app.decorators import permission_required

reviews = Blueprint("reviews", __name__)

@reviews.route("/review/<int:product_id>/<int:review_id>/delete",  methods=["GET", "POST"])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def delete_review(product_id, review_id):
	review = Review.query.get_or_404(review_id)
	if review.author != current_user:
		abort(403)
	product = Product.query.get_or_404(product_id)
	database.session.delete(review)
	database.session.commit()
	flash("Your post has been deleted!", "success")
	return redirect(url_for("products.product", product_id=product_id))
