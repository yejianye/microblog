import json
from functools import wraps

from flask import make_response, Response, request

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
