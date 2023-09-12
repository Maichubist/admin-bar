from flask import request

from functools import wraps

def required_auth(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not request.headers.get("Authorization"):
            return {"message": "unauthorized"}, 401
        
        return func(*args, **kwargs)
    return inner
