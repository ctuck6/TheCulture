from app import create_app
import flask_whooshalchemy as whooshalchemy
from app.models import Review, User
from flask import request, abort

app = create_app("development")
app.app_context().push()

IS_MAINTENANCE_MODE = False


@app.before_request
def check_for_maintenance():
    if IS_MAINTENANCE_MODE and not "static" in request.path:
        abort(503)

if __name__ == "__main__":
    whooshalchemy.whoosh_index(app, Review)
    whooshalchemy.whoosh_index(app, User)
    app.run(debug=True)
