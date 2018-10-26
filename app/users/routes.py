from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import database, bcrypt
from app.models import User, Review
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from app.users.utils import savePicture, sendResetEmail


users = Blueprint("users", __name__)

@users.route("/register", methods = ["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	form = RegistrationForm()
	if form.validate_on_submit():
		userName = User.query.filter_by(username = form.username.data).first()
		userEmail = User.query.filter_by(email = form.email.data).first()
		if userName:
			flash("Username already exists. Please try again", "danger")
		elif userEmail:
			flash("Email already exists. Please try again", "danger")
		else:
			hashed_password = bcrypt.generate_password_hash(form.password.data)
			user = User(firstname = form.firstname.data, lastname = form.lastname.data, username = form.username.data.lower(), email = form.email.data.lower(), password = hashed_password)
			database.session.add(user)
			database.session.commit()
			flash("Your account has been created! Please sign in!", "success")
			return redirect(url_for("users.login"))
	return render_template("register.html", form = form)

@users.route("/login", methods = ["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data.lower()).first()
		if not user:
			flash("Username does not exist. Please try again", "danger")
		elif not bcrypt.check_password_hash(user.password, form.password.data):
			flash("Incorrect password. Please try again", "danger")
		else:
		 	login_user(user, remember = form.remember.data)
		 	next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for("main.home"))
	return render_template("login.html", form = form)

@users.route("/reset_password", methods = ["GET", "POST"])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		sendResetEmail(user)
		flash("An email to reset your password has been sent to your email!", "success")
		return redirect(url_for("users.login"))
	return render_template("reset_request.html", form = form)

@users.route("/reset_password/<token>", methods = ["GET", "POST"])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	user = User.verify_reset_token(token)
	if not user:
		flash("Token enter is invalid or has expired!", "danger")
		return redirect(url_for("users.reset_request"))
	form = ResetPasswordForm()
	if form.validate_on_submit():
			hashed_password = bcrypt.generate_password_hash(form.password.data)
			user.password = hashed_password
			database.session.commit()
			flash("Your password has been updated! Please sign in!", "success")
			return redirect(url_for("users.login"))
	return render_template("reset_token.html", form = form)

@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("main.home"))

@users.route("/account", methods = ["GET", "POST"])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.profilePicture.data:
			oldPicture = User.query.get(int(current_user.id)).image_file
			newPicture = savePicture(form.profilePicture.data, oldPicture)
			current_user.image_file = newPicture
		if form.username.data != current_user.username:
			current_user.username = form.username.data.lower()
		if form.email.data != current_user.email:
			current_user.email = form.email.data.lower()
		database.session.commit()
		flash("Your account changes have been saved!", "success")
		return redirect(url_for("users.account"))
	elif request.method == "GET":
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template("account.html", form = form)

@users.route("/user/<string:username>")
def user_reviews(username):
	page = request.args.get("page", 1, type = int)
	user = User.query.filter_by(username = username).first_or_404()
	reviews = Review.query.filter_by(author = user).order_by(Review.date_posted.desc()).paginate(page = page, per_page = 5)
	return render_template("user_reviews.html", paginate = "user", reviews = reviews, user = user)