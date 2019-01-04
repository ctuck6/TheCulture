from flask import Blueprint, render_template, url_for, redirect, request
from app.models import User, Review
import os
from app.users.forms import SearchForm

main = Blueprint("main", __name__)
tables = [User, Review]

# from app.decorators import admin_required, permission_required
# from app.models import Permission
# @admin_required
# @permission_required(Permission.MODERATE_COMMENTS)


@main.route('/', methods=["GET", "POST"])
def home():
	top_reviews = Review.query.order_by(Review.views.desc()).limit(2).all()
	return render_template("home.html", top_reviews=top_reviews)


@main.route("/about")
def about():
	return render_template("about.html")


@main.route("/privacy")
def privacy():
	return render_template("privacy.html")


@main.route("/terms_of_use")
def terms_of_use():
	return render_template("terms_of_use.html")


@main.route("/search", methods=["GET", "POST"])
@main.route("/search/<string:keyword>", methods=["GET", "POST"])
def search_keyword(keyword=None):
	form = SearchForm()
	results = list()
	if form.validate_on_submit():
		return redirect(url_for("main.search_keyword", keyword=form.search.data))
	if keyword:
		for table in tables:
			search = table.query.whoosh_search(keyword).all()
			for result in search:
				results.append(result)
	return render_template("search.html", form=form, keyword=keyword, results=results)
