##############################################################################################################
# likes/routes.py
##############################################################################################################

from flask import Blueprint, render_template, request
from flask_login import login_required
from app import database
from app.models import Like, Permission, Article
from app.decorators import permission_required

likes = Blueprint("likes", __name__)


@likes.route("/article/like", methods=["GET", "POST"])
@login_required
@permission_required(Permission.COMMENT)
def like():
	like = Like(user_id=request.form.get("user_id"), article_id=request.form.get("article_id"))
	article = Article.query.get(request.form.get("article_id"))
	database.session.add(like)
	database.session.commit()
	return render_template("jquery/like.html", like=like, article=article)


@likes.route("/article/unlike", methods=["GET", "POST"])
@login_required
@permission_required(Permission.COMMENT)
def unlike():
	like = Like.query.get(request.form.get("like_id"))
	article = Article.query.get(request.form.get("article_id"))
	database.session.delete(like)
	database.session.commit()
	return render_template("jquery/unlike.html", article=article)
