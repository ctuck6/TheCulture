##############################################################################################################
# articles/routes.py
##############################################################################################################

from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import database
from app.models import Article, Comment, Company, Permission
from app.articles.forms import ArticleForm
from app.comments.forms import CommentForm
from app.decorators import permission_required

articles = Blueprint("articles", __name__)


@articles.route("/article/<int:article_id>", methods=["GET", "POST"])
def article(article_id):
	article = Article.query.get_or_404(article_id)
	if article:
		article.views += 1
		database.session.commit()
	comments = Comment.query.filter_by(article=article).order_by(Comment.date_posted).all()
	form = CommentForm()
	if form.validate_on_submit():
		comment = Comment(body=form.body.data, article=article, commenter=current_user._get_current_object())
		database.session.add(comment)
		database.session.commit()
		flash("Your comment has been posted!", "success")
		return redirect(url_for('articles.article', article_id=article_id))
	return render_template("article.html", article=article, form=form, comments=comments)


@articles.route("/article/<int:article_id>/delete",  methods=["GET", "POST"])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def delete_article(article_id):
	article = Article.query.get_or_404(article_id)
	if article.author != current_user:
		abort(403)
	database.session.delete(article)
	database.session.commit()
	flash("Your post has been deleted!", "success")
	return redirect(url_for("articles.show_articles"))


@articles.route("/article/new", methods=["GET", "POST"])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def new_article():
	form = ArticleForm()
	if form.validate_on_submit():
		if not form.validate_title(form.title):
			flash("Article title already being used. Please try again", "danger")
		else:
			company = Company.query.filter_by(name=form.company.data).first()
			article = Article(title=form.title.data, body=form.body.data, author=current_user._get_current_object(), company=company)
			database.session.add(article)
			database.session.commit()
			flash("Your article has been posted!", "success")
			article = Article.query.filter_by(title=form.title.data).first_or_404()
			return redirect(url_for("articles.article", article_id=article.id))
	return render_template("new_article.html", legend="New Article", form=form)


@articles.route("/articles", methods=["GET", "POST"])
def show_articles():
	page = request.args.get("page", 1, type=int)
	articles = Article.query.order_by(Article.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template("show_articles.html", paginate="all", articles=articles)


@articles.route("/article/<int:article_id>/update",  methods=["GET", "POST"])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def update_article(article_id):
	article = Article.query.get_or_404(article_id)
	if article.author != current_user:
		abort(403)
	form = ArticleForm()
	if form.validate_on_submit():
		article.title = form.title.data
		article.body = form.body.data
		article.company = Company.query.filter_by(name=form.company.data).first()
		database.session.commit()
		flash("Your post has been updated!", "success")
		return redirect(url_for("articles.article", article_id=article.id))
	elif request.method == "GET":
		form.title.data = article.title
		form.body.data = article.body
		if article.company:
			form.company.data = article.company.name
	return render_template("new_article.html", legend="Update Article", form=form)
