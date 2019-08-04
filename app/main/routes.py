##############################################################################################################
# main/routes.py
##############################################################################################################

from flask import Blueprint, render_template, url_for, redirect, g
from app.models import Company, Product, User, Article
from app.utils import generate_header_picture
from app.constants import Constants

main = Blueprint("main", __name__)
tables = [User, Article, Company, Product]


@main.route("/about")
def about():
	picture = generate_header_picture()
	return render_template("about.html", picture=picture)


@main.route("/contact")
def contact():
	return render_template("contact.html")


@main.route('/', methods=["GET", "POST"])
def home():
	picture = generate_header_picture()
	articles = Article.query.order_by(Article.views.desc()).limit(Constants.ARTICLES_ON_HOME_PAGE).all()
	return render_template("index.html", articles=articles, picture=picture)


@main.route("/privacy")
def privacy():
	return render_template("privacy.html")


@main.route("/register")
def register():
	return render_template("register.html")


@main.route("/search")
def search():
	if not g.search_form.validate():
		return redirect(url_for('main.home'))
	results = list()
	keyword = g.search_form.search.data
	for table in tables:
		search = table.query.whoosh_search(keyword).all()
		for result in search:
			results.append(result)
	return render_template("search.html", results=results)


@main.route("/terms_of_use")
def terms_of_use():
	return render_template("terms_of_use.html")
