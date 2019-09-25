##############################################################################################################
# comments/forms.py
##############################################################################################################

from flask import Blueprint, abort, request, render_template
from flask_login import current_user, login_required
from app import database
from app.models import Article, Comment, Permission
from app.decorators import permission_required
from app.constants import Constants

comments = Blueprint("comments", __name__)


@comments.route("/comment/delete", methods=["GET", "POST"])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def delete_comment():
	article = Article.query.get_or_404(request.form.get('article_id'))
	comment = Comment.query.get_or_404(request.form.get('comment_id'))
	comment_count = request.form.get('count')
	if comment.commenter != current_user and current_user != article.author:
		abort(Constants.FORBIDDEN_PAGE_ERROR_PAGE)
	database.session.delete(comment)
	database.session.commit()
	comments = Comment.query.filter_by(article_id=article.id).limit(comment_count).all()
	return render_template('jquery/comment.html', article=article, comments=comments)


@comments.route("/comment/load", methods=["GET", "POST"])
def load_more_comments():
	article = Article.query.get_or_404(request.form.get('article_id'))
	comment_count = int(request.form.get('count'))
	comments = Comment.query.filter_by(article_id=article.id).limit(comment_count + Constants.COMMENTS_PER_ARTICLE).all()
	return render_template("jquery/comment.html", comments=comments, article=article)


@comments.route("/comment/post", methods=["GET", "POST"])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def post_comment():
	article = Article.query.get_or_404(request.form.get('article_id'))
	comment_count = request.form.get('count')
	comment = Comment(body=request.form.get('comment_body'), article=article, commenter=current_user._get_current_object())
	database.session.add(comment)
	database.session.commit()
	comments = Comment.query.filter_by(article_id=article.id).limit(int(comment_count) + 1).all()
	return render_template("jquery/comment.html", article=article, comments=comments)