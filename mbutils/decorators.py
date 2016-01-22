from functools import wraps

def singleton(func):
    @wraps(func)
    def _func(*args, **kwargs):
        if not hasattr(_func, '_singleton'):
            _func._singleton = _func(*args, **kwargs)
        return _func._singleton
    return _func
