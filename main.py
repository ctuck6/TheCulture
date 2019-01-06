from app import create_app
import flask_whooshalchemy as whooshalchemy
from app.models import Review, User
from flask import request, abort, current_app
from app.config import ProductionConfig
import os

app = create_app(os.environ.get("APP_SETTINGS"))
app.app_context().push()


@app.before_request
def check_for_maintenance():
    if ProductionConfig.MAINTENANCE_MODE and not "static" in request.path:
        abort(503)

if __name__ == "__main__":
    whooshalchemy.whoosh_index(app, Review)
    whooshalchemy.whoosh_index(app, User)
    app.run(debug=True)
