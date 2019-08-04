##############################################################################################################
# comments/forms.py
##############################################################################################################

from flask import Blueprint, url_for, flash, redirect, abort, request, render_template
from flask_login import current_user, login_required
from app import database
from app.models import Article, Comment, Permission
from app.decorators import permission_required
from app.constants import Constants

comments = Blueprint("comments", __name__)


@comments.route("/comment/<int:article_id>/<int:comment_id>/delete", methods=["GET", "POST"])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def delete_comment(article_id, comment_id):
	article = Article.query.get_or_404(article_id)
	comment = Comment.query.get_or_404(comment_id)
	if comment.commenter != current_user and current_user != article.author:
		abort(Constants.FORBIDDEN_PAGE_ERROR_PAGE)
	database.session.delete(comment)
	database.session.commit()
	flash("Your comment has been deleted!", "success")
	return redirect(url_for("articles.article", article_id=article_id))


@comments.route("/comment/save", methods=["GET", "POST"])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def save_comment():
	article = Article.query.get_or_404(request.form.get('article_id'))
	comment = Comment.query.get_or_404(request.form.get('comment_id'))
	comment.body = request.form.get('body')
	database.session.commit()
	return render_template("jquery/comment.html", comment=comment, article=article)


@comments.route("/comment/update", methods=["POST"])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def update_comment():
	article = Article.query.get_or_404(request.form.get('article_id'))
	comment = Comment.query.get_or_404(request.form.get('comment_id'))
	return render_template("jquery/comment_form.html", comment=comment, article=article)
