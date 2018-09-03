from flask import Blueprint, render_template, url_for, current_app
import os

main = Blueprint("main", __name__)

@main.route('/')
@main.route("/home")
def home():
	pictures = os.listdir("app/static/slideshowPics")
	return render_template("home.html", pictures = pictures)

@main.route("/about")
def about():
	return render_template("about.html")