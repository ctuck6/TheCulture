from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.database import Review
from app.reviews.forms import ReviewForm

reviews = Blueprint("reviews", __name__)

@reviews.route("/reviews", methods = ["GET", "POST"])
def show_reviews():
	page = request.args.get("page", 1, type=int)
	reviews = Review.query.order_by(Review.date_posted.desc()).paginate(page = page, per_page = 5)
	return render_template("reviews.html", reviews = reviews)

@reviews.route("/review/<int:review_id>")
def review(review_id):
	review = Review.query.get_or_404(review_id)
	return render_template("review.html", review = review)

@reviews.route("/review/<int:review_id>/update",  methods = ["GET", "POST"])
@login_required
def update_review(review_id):
	review = Review.query.get_or_404(review_id)
	if review.author != current_user:
		abort(403)
	form = ReviewForm()
	if form.validate_on_submit():
		review.title = form.title.data
		review.body = form.body.data
		db.session.commit()
		flash("Your post has been updated!", "success")
		return redirect(url_for("reviews.review", review_id = review.id))
	elif request.method == "GET":
		form.title.data = review.title
		form.body.data = review.body
	return render_template("create_review.html", legend = "Update Review", form = form)

@reviews.route("/review/<int:review_id>/delete",  methods = ["POST"])
@login_required
def delete_review(review_id):
	review = Review.query.get_or_404(review_id)
	if review.author != current_user:
		abort(403)
	db.session.delete(review)
	db.session.commit()
	flash("Your post has been deleted!", "success")
	return redirect(url_for("reviews.show_reviews"))

@reviews.route("/review/new", methods = ["GET", "POST"])
@login_required
def new_review():
	form = ReviewForm()
	if form.validate_on_submit():
		review = Review(title = form.title.data, body = form.body.data, author = current_user)
		db.session.add(review)
		db.session.commit()
		flash("Your review has been posted!", "success")
		return redirect(url_for("reviews.show_reviews"))
	return render_template("create_review.html", legend = "New Review", form = form)

@reviews.route("/latest_reviews", methods = ["GET", "POST"])
def latest_reviews():
	reviews = Review.query.order_by(Review.date_posted.desc()).paginate(page = 1, per_page = 10)
	return render_template("latest_reviews.html", reviews = reviews)