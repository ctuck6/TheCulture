from flask import Blueprint, render_template, url_for, redirect
# from app import database
from app.models import User, Review
# from sqlalchemy_searchable import search
import os
from app.users.forms import SearchForm
# import flask_whooshalchemyplus

main = Blueprint("main", __name__)
tables = [User, Review]


@main.route('/', methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home():
	pictures = os.listdir("app/static/slideshowPics")
	top_reviews = Review.query.order_by(Review.views.desc()).limit(2).all()
	latest_reviews = Review.query.order_by(Review.date_posted.desc()).limit(5).all()
	return render_template("home.html", latest_reviews=latest_reviews, top_reviews=top_reviews, pictures=pictures)

@main.route("/about")
def about():
	return render_template("about.html")

@main.route("/privacy")
def privacy():
	return render_template("privacy.html")

@main.route("/terms_of_use")
def terms_of_use():
	return render_template("terms_of_use.html")

@main.route("/search_results/<keyword>", methods=["GET"])
def search_results(keyword):
	results = list()
	for table in tables:
		search = table.query.whoosh_search(keyword).all()
		for result in search:
			results.append(result)
	return render_template("search_results.html", results=results)


@main.route("/search", methods=["GET", "POST"])
def search_keyword():
	form = SearchForm()
	if form.validate_on_submit():
		return redirect(url_for("main.search_results", keyword=form.search.data))
	return render_template("search.html", form=form)
