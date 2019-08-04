from functools import wraps
from flask import abort
from flask_login import current_user
from app.constants import Constants


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(Constants.FORBIDDEN_PAGE_ERROR_PAGE)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
