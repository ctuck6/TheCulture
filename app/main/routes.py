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
@main.route("/home", methods=["GET", "POST"])
def home():
	pictures = os.listdir("app/static/slideshowPics")
	top_reviews = Review.query.order_by(Review.views.desc()).limit(2).all()
	return render_template("home.html", top_reviews=top_reviews, pictures=pictures)


@main.route("/about")
def about():
	return render_template("about.html")


@main.route("/privacy")
def privacy():
	return render_template("privacy.html")


@main.route("/terms_of_use")
def terms_of_use():
	return render_template("terms_of_use.html")


@main.route("/search_results", methods=["GET", "POST"])
def search_results():
	keyword = request.form.get("keyword", None)
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
