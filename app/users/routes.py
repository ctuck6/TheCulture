##############################################################################################################
# users/routes.py
##############################################################################################################

from uuid import uuid4
from flask import Blueprint, render_template, url_for, flash, redirect, request, g, abort
from flask_login import login_user, current_user, login_required, logout_user, fresh_login_required, login_fresh
from app import database, bcrypt, login_manager
from app.models import User, Article, MailingList, Product, Company
from app.users.forms import LoginForm, RegistrationForm, UpdateAccountForm, UpdatePasswordForm, UpdatePictureForm, \
	RequestResetForm, ResetPasswordForm
from app.utils import send_reset_email, upload_to_s3, remove_from_s3, generate_header_picture
from app.config import Config
from app.constants import Constants

users = Blueprint("users", __name__)


@users.route("/account/information/<string:username>", methods=["GET", "POST"])
@fresh_login_required
def account(username):
	if current_user.is_company or current_user.username != username:
		abort(Constants.FORBIDDEN_PAGE_ERROR_PAGE)

	user = User.query.filter_by(username=username).first_or_404()
	account_form = UpdateAccountForm()
	password_form = UpdatePasswordForm()
	picture_form = UpdatePictureForm()

	if picture_form.submit_picture.data and picture_form.validate_on_submit():
		if picture_form.image_file.data:
			remove_from_s3(user.username,
						picture_form.image_file.data.filename,
						"profilePics",
						Config.AWS_STORAGE_BUCKET_NAME)
			new_picture = upload_to_s3(user.username,
									picture_form.image_file.data,
									"profilePics",
									Config.AWS_STORAGE_BUCKET_NAME,
									Constants.PROFILE_PICTURE_SIZE)
			user.image_file = new_picture
			database.session.commit()
			flash("Your profile picture has been changed!", "success")

		return redirect(url_for('users.account', username=user.username))

	if account_form.submit_info.data and account_form.validate_on_submit():
		valid_input = True

		if account_form.firstname.data and account_form.firstname.data != user.firstname:
			user.firstname = account_form.firstname.data

		if account_form.lastname.data and account_form.lastname.data != user.lastname:
			user.lastname = account_form.lastname.data

		if account_form.username.data and account_form.validate_username(account_form.username):
			user.username = account_form.username.data.lower()
		else:
			valid_input = False
			flash("Username already being used. Please try again", "danger")

		if account_form.validate_email(account_form.email):
			user.email = account_form.email.data.lower()
		else:
			valid_input = False
			flash("Email already being used. Please try again", "danger")

		if account_form.validate_phone_number(account_form.phone_number):
			user.phone_number = account_form.phone_number.data
		else:
			valid_input = False
			flash("Phone number already being used. Please try again", "danger")

		if account_form.occupation.data and account_form.occupation.data != user.occupation:
			user.occupation = account_form.occupation.data

		if account_form.hometown.data and account_form.hometown.data != user.hometown:
			user.hometown = account_form.hometown.data

		if account_form.bio.data and account_form.bio.data != user.bio:
			user.bio = account_form.bio.data

		if valid_input:
			database.session.commit()
			flash("Your account changes have been saved!", "success")

		return redirect(url_for('users.account', username=user.username))

	if password_form.submit_password.data and password_form.validate_on_submit():
		valid_input = True

		if password_form.validate_password(password_form.old_password):
			hashed_password = bcrypt.generate_password_hash(password_form.new_password.data)
			user.password = hashed_password
		else:
			valid_input = False
			flash("Incorrect old password. Please try again", "danger")

		if valid_input:
			database.session.commit()
			flash("Your password has been changed!", "success")

		return redirect(url_for('users.account', username=user.username))

	if request.method == "GET":
		account_form.firstname.data = user.firstname
		account_form.lastname.data = user.lastname
		account_form.username.data = user.username
		account_form.email.data = user.email
		account_form.phone_number.data = user.phone_number
		account_form.occupation.data = user.occupation
		account_form.hometown.data = user.hometown
		account_form.bio.data = user.bio

	return render_template("account_user.html", user=user, account_form=account_form, password_form=password_form, picture_form=picture_form)


@users.route("/wishlist/add/<user_id>/<int:product_id>",  methods=["GET", "POST"])
@login_required
def add_to_wishlist(user_id, product_id):
	user = User.query.get_or_404(user_id)
	product = Product.query.get_or_404(product_id)
	user.wishlist.append(product)
	database.session.commit()

	return redirect(url_for("products.product", product_id=product_id))


@users.route("/deactivate/<user_id>")
@login_required
def deactivate(user_id):
	user = User.query.get_or_404(user_id)
	database.session.delete(user)
	database.session.commit()

	return redirect(url_for("main.home"))


@login_manager.user_loader
def load_user(user_id):
	company = Company.query.get(user_id)

	if not company:
		return User.query.get(user_id)

	return company


@users.route("/login/user", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated and login_fresh():
		return redirect(url_for("main.home"))

	form = LoginForm()
	picture = generate_header_picture()

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

	return render_template("login.html", form=form, picture=picture, current_login_type="personal account", needed_login_type="company")


@users.route("/logout")
@login_required
def logout():
	logout_user()

	return redirect(url_for("main.home"))


@users.route("/wishlist/delete/<user_id>/<int:product_id>",  methods=["GET", "POST"])
@login_required
def remove_from_wishlist(user_id, product_id):
	user = User.query.get_or_404(user_id)
	product = Product.query.get_or_404(product_id)
	user.wishlist.remove(product)
	database.session.commit()

	return redirect(request.referrer)


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
		flash("Token is invalid or has expired!", "danger")

		return redirect(url_for("users.reset_request"))

	form = ResetPasswordForm()

	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data)
		user.password = hashed_password
		database.session.commit()
		flash("Your password has been updated! Please sign in!", "success")

		return redirect(url_for("users.login"))

	return render_template("reset_token.html", form=form)


@users.route("/subscribe")
@login_required
def subscribe():
	if not g.subscribe_form.validate():
		return redirect(url_for('main.home'))

	email = g.subscribe_form.subscribe.data
	subscriber = MailingList(email=email)
	database.session.add(subscriber)
	database.session.commit()

	return render_template("subscribe.html")


@users.route("/unsubscribe", methods=["GET", "POST"])
@login_required
def unsubscribe():
	form = RequestResetForm()

	if form.validate_on_submit():
		email = MailingList.query.filter_by(email=form.email.data.lower()).first()

		if email:
			database.session.delete(email)
			database.session.commit()
			flash("You have successfully unsubscribed!", "success")
		else:
			flash("Email does not exist!", "danger")

	return render_template("unsubscribe.html", form=form)


@users.route("/account/articles/<string:username>", methods=["GET", "POST"])
@login_required
def user_articles(username):
	if current_user.is_company or current_user.username != username:
		abort(Constants.FORBIDDEN_PAGE_ERROR_PAGE)

	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get("page", 1, type=int)
	articles = Article.query.filter_by(author=user).order_by(Article.date_posted.desc())\
			.paginate(page=page, per_page=Constants.ARTICLES_PER_USER_ARTICLES_PAGE)
	prev_page = url_for('users.user_articles', username=username, page=articles.prev_num)
	next_page = url_for('users.user_articles', username=username, page=articles.next_num)

	return render_template("account_articles.html", paginate=True, user=user,
							articles=articles, prev_page=prev_page, next_page=next_page)


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
			user_id = unicode(uuid4())
			user = User(id=user_id,
						firstname=form.firstname.data,
						lastname=form.lastname.data,
						username=form.username.data.lower(),
						email=form.email.data.lower(),
						password=hashed_password)
			database.session.add(user)
			database.session.commit()
			flash("Your account has been created! Please sign in!", "success")

			return redirect(url_for("users.login"))

	return render_template("register_user.html", form=form)


@users.route("/wishlist/<string:username>", methods=["GET", "POST"])
@login_required
def wishlist(username):
	user = User.query.filter_by(username=username).first_or_404()
	total = sum([float(product.price) for product in user.wishlist.all()])
	total = "${:,.2f}".format(total)

	return render_template("wishlist.html", total=total, user=user)
