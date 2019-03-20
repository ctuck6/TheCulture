##############################################################################################################
# main/routes.py
##############################################################################################################

from flask import Blueprint, render_template, url_for, redirect, request
from app.models import Company, Product, User, Article
import os
from app.main.forms import SearchForm

main = Blueprint("main", __name__)
tables = [User, Article, Company, Product]


@main.route("/about")
def about():
	return render_template("about.html")


@main.route('/', methods=["GET", "POST"])
def home():
	top_articles = Article.query.order_by(Article.views.desc()).limit(2).all()
	return render_template("home.html", top_articles=top_articles)


@main.route("/privacy")
def privacy():
	return render_template("privacy.html")


@main.route("/register")
def register():
	return render_template("register.html")


@main.route("/search", methods=["GET", "POST"])
@main.route("/search/<string:keyword>", methods=["GET", "POST"])
def search(keyword=None):
	form = SearchForm()
	results = list()
	if form.validate_on_submit():
		return redirect(url_for("main.search", keyword=form.search.data))
	if keyword:
		for table in tables:
			search = table.query.whoosh_search(keyword).all()
			for result in search:
				results.append(result)
	return render_template("search.html", form=form, keyword=keyword, results=results)


@main.route("/terms_of_use")
def terms_of_use():
	return render_template("terms_of_use.html")
