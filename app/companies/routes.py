from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user
from app import database, bcrypt
from uuid import uuid4
from app.models import Company
from app.utils import generate_header_picture
from app.companies.forms import RegistrationForm
from app.users.forms import LoginForm
from app.constants import Constants

companies = Blueprint("companies", __name__)


@companies.route("/register/company", methods=["GET", "POST"])
def company_register():
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	form = RegistrationForm()
	if form.validate_on_submit():
		if not form.validate_email(form.email):
			flash("Email already being used. Please try again", "danger")
		elif not form.validate_address(form.address):
			flash("Address already being used. Please try again", "danger")
		elif not form.validate_phone_number(form.phone_number):
			flash("Phone number already being used. Please try again", "danger")
		elif not form.validate_website(form.website):
			flash("Website already being used. Please try again", "danger")
		else:
			hashed_password = bcrypt.generate_password_hash(form.password.data)
			user_id = unicode(uuid4())
			company = Company(id=user_id,
						name=form.name.data.lower(),
                        address=form.address.data.lower(),
                        city=form.city.data.lower(),
                        zip_code=form.zip_code.data,
                        state=form.state.data,
                        country=form.country.data,
                        phone_number=form.phone_number.data,
                        email=form.email.data.lower(),
                        website=form.website.data.lower(),
                        password=hashed_password)
			database.session.add(company)
			database.session.commit()
			flash("Your company has been registered! Please sign in!", "success")
			return redirect(url_for("companies.login"))
	return render_template("register_company.html", form=form)


@companies.route("/company/<company_id>", methods=["GET", "POST"])
def company(company_id):
	company = Company.query.get_or_404(company_id)
	return render_template("company.html", company=company)


@companies.route("/login/company", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	form = LoginForm()
	if form.validate_on_submit():
		company = Company.query.filter_by(email=form.email.data.lower()).first()
		if not form.validate_email(form.email):
			flash("Email does not exist. Please try again", "danger")
		elif not bcrypt.check_password_hash(company.password, form.password.data):
			flash("Incorrect password. Please try again", "danger")
		else:
			login_user(company, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for("main.home"))
	return render_template("login.html", form=form, current_login_type="company", needed_login_type="personal account")


@companies.route("/companies", methods=["GET", "POST"])
def show_companies():
	picture = generate_header_picture()
	page = request.args.get("page", 1, type=int)
	companies = Company.query.paginate(page=page, per_page=Constants.COMPANIES_ON_SHOW_COMPANIES_PAGE)
	prev_page = url_for('companies.show_companies', page=companies.prev_num)
	next_page = url_for('companies.show_companies', page=companies.next_num)
	return render_template("show_companies.html", picture=picture, paginate=True,
							companies=companies, prev_page=prev_page, next_page=next_page)
