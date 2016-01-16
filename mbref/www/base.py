import json
from functools import wraps

from flask import make_response, Response, request

def route(*args, **kwargs):
    def _route(func):
        func._flask_route = {
            'args': args,
            'kwargs': kwargs
        }
        return func
    return _route

def load_views(app, module):
    for name in dir(module):
        view = getattr(module, name)
        if hasattr(view, '_flask_route'):
            spec = view._flask_route
            app.route(*spec['args'], **spec['kwargs'])(view)

def json_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, Response):
            return result
        else:
            response = make_response(json.dumps(result))
            response.headers['Content-Type'] = 'application/json'
            return response
    return wrapper
