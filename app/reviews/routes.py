from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import database
from app.models import Review, Comment
from app.reviews.forms import ReviewForm, CommentForm

reviews = Blueprint("reviews", __name__)


@reviews.route("/reviews", methods=["GET", "POST"])
def show_reviews():
	page = request.args.get("page", 1, type=int)
	reviews = Review.query.order_by(Review.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template("show_reviews.html", paginate="all", reviews=reviews)


@reviews.route("/review/<int:review_id>", methods=["GET", "POST"])
def review(review_id):
	review = Review.query.get_or_404(review_id)
	# if review:
	# 	review.views += 1
	# 	database.session.commit()
	comments = Comment.query.filter_by(review=review).order_by(Comment.date_posted.desc()).all()
	form = CommentForm()
	if form.validate_on_submit():
		if current_user.is_authenticated:
			comment = Comment(body=form.body.data, review=review, commenter=current_user.username)
			database.session.add(comment)
			database.session.commit()
			flash("Your comment has been posted!", "success")
			return redirect(url_for('reviews.review', review_id=review_id))
		else:
			flash("You must be logged in to post a comment!", "danger")
			abort(403)
	return render_template("review.html", review=review, form=form, comments=comments)


@reviews.route("/review/new", methods=["GET", "POST"])
@login_required
def new_review():
	form = ReviewForm()
	if form.validate_on_submit():
		review = Review(title=form.title.data, body=form.body.data, author=current_user)
		database.session.add(review)
		database.session.commit()
		flash("Your review has been posted!", "success")
		return redirect(url_for("reviews.show_reviews"))
	return render_template("new_review.html", legend="New Review", form=form)


@reviews.route("/review/<int:review_id>/update",  methods=["GET", "POST"])
@login_required
def update_review(review_id):
	review = Review.query.get_or_404(review_id)
	if review.author != current_user:
		abort(403)
	form = ReviewForm()
	if form.validate_on_submit():
		review.title = form.title.data
		review.body = form.body.data
		database.session.commit()
		flash("Your post has been updated!", "success")
		return redirect(url_for("reviews.review", review_id=review.id))
	elif request.method == "GET":
		form.title.data = review.title
		form.body.data = review.body
	return render_template("new_review.html", legend="Update Review", form=form)


@reviews.route("/review/<int:review_id>/delete",  methods=["GET", "POST"])
@login_required
def delete_review(review_id):
	review = Review.query.get_or_404(review_id)
	if review.author != current_user:
		abort(403)
	database.session.delete(review)
	database.session.commit()
	flash("Your post has been deleted!", "success")
	return redirect(url_for("reviews.show_reviews"))
