from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user
from app import database, bcrypt
from app.models import Company
from app.companies.forms import RegistrationForm

companies = Blueprint("companies", __name__)


@companies.route("/register/company", methods=["GET", "POST"])
def company_register():
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	form = RegistrationForm()
	if form.validate_on_submit():
		if not form.validate_username(form.email):
			flash("Email already being used. Please try again", "danger")
		elif not form.validate_email(form.address):
			flash("Address already being used. Please try again", "danger")
		elif not form.validate_phone_number(form.phone_number):
			flash("Phone number already being used. Please try again", "danger")
		else:
			hashed_password = bcrypt.generate_password_hash(form.password.data)
			company = Company(name=form.name.data.lower(),
                        address=form.address.data.lower(),
                        city=form.city.data.lower(),
                        zip_code=form.zip_code.data,
                        state=form.state.data,
                        country=form.country.data,
                        phone_number=form.phone_number.data,
                        email=form.email.data.lower(),
                        password=hashed_password)
			database.session.add(company)
			database.session.commit()
			flash("Your company has been registered! Please sign in!", "success")
			return redirect(url_for("companies.company_login"))
	return render_template("register_company.html", form=form)
