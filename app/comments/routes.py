from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import database
from app.models import Review, Comment

comments = Blueprint("comments", __name__)

@comments.route("/review/<int:review_id>/<int:comment_id>/delete",  methods=["GET", "POST"])
@login_required
def delete_comment(review_id, comment_id):
	review = Review.query.get_or_404(review_id)
	comment = Comment.query.get_or_404(comment_id)
	if comment.commenter != current_user and current_user != review.author:
		abort(403)
	database.session.delete(comment)
	database.session.commit()
	flash("The comment has been deleted!", "success")
	return redirect(url_for("reviews.review", review_id=review_id))
