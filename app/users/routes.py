##############################################################################################################
# users/routes.py
##############################################################################################################

from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import database, bcrypt
from app.models import User, Review, Role, Article
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, AdminForm
from app.main.forms import SearchForm
from app.utils import save_picture, send_reset_email
from app.decorators import admin_required


users = Blueprint("users", __name__)


@users.route("/account/<string:username>", methods=["GET", "POST"])
@login_required
def account(username):
	user = User.query.filter_by(username=username).first_or_404()
	form = UpdateAccountForm()
	valid_input = True
	if form.validate_on_submit():
		if form.image_file.data:
			old_picture = user.image_file
			new_picture = save_picture(form.image_file.data, old_picture)
			current_user.image_file = new_picture
		if form.validate_username(form.username):
			current_user.username = form.username.data.lower()
		else:
			valid_input = False
			flash("Username already being used. Please try again", "danger")
		if form.validate_email(form.email):
			current_user.email = form.email.data.lower()
		else:
			valid_input = False
			flash("Email already being used. Please try again", "danger")
		if form.validate_phone_number(form.phone_number):
			current_user.phone_number = form.phone_number.data
		else:
			valid_input = False
			flash("Phone number already being used. Please try again", "danger")
		if form.occupation.data and form.occupation.data != current_user.occupation:
			current_user.occupation = form.occupation.data
		if form.bio.data and form.bio.data != current_user.bio:
			current_user.bio = form.bio.data
		if valid_input:
			database.session.commit()
			flash("Your account changes have been saved!", "success")
		return redirect(url_for('users.account', username=user.username))
	elif request.method == "GET":
		form.firstname.data = current_user.firstname
		form.lastname.data = current_user.lastname
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.phone_number.data = current_user.phone_number
		form.occupation.data = current_user.occupation
		form.bio.data = current_user.bio
	page = request.args.get("page", 1, type=int)
	articles = Article.query.filter_by(author=user).order_by(Article.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template("account.html", paginate="user", user=user, articles=articles, form=form)


@users.route("/admin_settings", methods=["GET", "POST"])
@users.route("/admin_settings/<string:username>", methods=["GET", "POST"])
@login_required
@admin_required
def admin_settings(username=None):
	search_form = SearchForm()
	role_form = AdminForm()
	user = User.query.filter_by(username=username).first()
	if search_form.validate_on_submit():
		user = User.query.filter_by(username=search_form.search.data.lower()).first()
		if user:
			return redirect(url_for("users.admin_settings", username=user.username))
	if role_form.validate_on_submit():
		user.role = Role.query.filter_by(name=role_form.role.data).first()
		database.session.commit()
	return render_template("admin_settings.html", searchForm=search_form, roleForm=role_form, user=user)


@users.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data.lower()).first()
		if not form.validate_email(form.email):
			flash("Email does not exist. Please try again", "danger")
		elif not bcrypt.check_password_hash(user.password, form.password.data):
			flash("Incorrect password. Please try again", "danger")
		else:
		 	login_user(user, remember=form.remember.data)
		 	next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for("main.home"))
	return render_template("login.html", form=form)


@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("main.home"))


@users.route("/register/user", methods=["GET", "POST"])
def user_register():
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	form = RegistrationForm()
	if form.validate_on_submit():
		if not form.validate_username(form.username):
			flash("Username already being used. Please try again", "danger")
		elif not form.validate_email(form.email):
			flash("Email already being used. Please try again", "danger")
		else:
			hashed_password = bcrypt.generate_password_hash(form.password.data)
			user = User(firstname=form.firstname.data,
						lastname=form.lastname.data,
						username=form.username.data.lower(),
						email=form.email.data.lower(),
						password=hashed_password)
			database.session.add(user)
			database.session.commit()
			flash("Your account has been created! Please sign in!", "success")
			return redirect(url_for("users.login"))
	return render_template("register_user.html", form=form)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	form = RequestResetForm()
	if form.validate_on_submit():
		if form.validate_email(form.email):
			user = User.query.filter_by(email=form.email.data.lower()).first()
			send_reset_email(user)
			flash("An email to reset your password has been sent to your email!", "success")
			return redirect(url_for("users.login"))
		else:
			flash("Email does not exist!", "danger")
	return render_template("reset_request.html", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
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
	return render_template("reset_token.html", form=form)
