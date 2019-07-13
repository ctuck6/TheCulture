from app import create_app
import flask_whooshalchemy as whooshalchemy
from app.models import Company, Product, Article, User, Role
from flask import request, abort, current_app, g
from app.config import ProductionConfig
from app.main.forms import SearchForm
from app.users.forms import SubscribeForm
from flask_login import current_user
import os
from app.constants import Constants

app = create_app()
app.app_context().push()

@app.before_request
def before_request():
	g.subscribe_form = SubscribeForm()
	if ProductionConfig.MAINTENANCE_MODE and not "static" in request.path:
		abort(Constants.MAINTENANCE_PAGE)
	elif ProductionConfig.COMING_SOON and not "static" in request.path:
		abort(Constants.COMING_SOON_PAGE)
	else:
		g.search_form = SearchForm()


if __name__ == "__main__":
	whooshalchemy.whoosh_index(app, Company)
	whooshalchemy.whoosh_index(app, Product)
	whooshalchemy.whoosh_index(app, Article)
	whooshalchemy.whoosh_index(app, User)
	app.run(debug=True)
