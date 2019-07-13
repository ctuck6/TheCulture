from flask import Blueprint, render_template
from app.utils import generate_header_picture
from app.constants import Constants

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(Constants.BAD_REQUEST_ERROR_PAGE)
def error_400(error):
	picture = generate_header_picture()
	return render_template('errors/400.html', picture=picture), Constants.BAD_REQUEST_ERROR_PAGE

@errors.app_errorhandler(Constants.COMING_SOON_PAGE)
def coming_soon(error):
	picture = generate_header_picture()
	return render_template('errors/coming_soon.html', picture=picture), Constants.COMING_SOON_PAGE

@errors.app_errorhandler(Constants.FORBIDDEN_PAGE_ERROR_PAGE)
def error_403(error):
	picture = generate_header_picture()
	return render_template('errors/403.html', picture=picture), Constants.FORBIDDEN_PAGE_ERROR_PAGE

@errors.app_errorhandler(Constants.PAGE_NOT_FOUND_ERROR_PAGE)
def error_404(error):
	picture = generate_header_picture()
	return render_template('errors/404.html', picture=picture), Constants.PAGE_NOT_FOUND_ERROR_PAGE

@errors.app_errorhandler(Constants.INTERNAL_SERVER_ERROR_PAGE)
def error_500(error):
	picture = generate_header_picture()
	return render_template('errors/500.html', picture=picture), Constants.INTERNAL_SERVER_ERROR_PAGE

@errors.app_errorhandler(Constants.MAINTENANCE_PAGE)
def maintenance(error):
	picture = generate_header_picture()
	return render_template('errors/maintenance.html', picture=picture), Constants.MAINTENANCE_PAGE
