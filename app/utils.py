from flask import jsonify
from flask.ext.login import current_user
from functools import wraps


def compose_json_error(errors):
    return_json = {'status': 'error'}
    if errors:
        return_json['errors'] = errors
    return jsonify(return_json)


def admin_priveleges_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        else:
            return compose_json_error({'Backend error': 'You are not admin, write restricted'})
    return wrapped