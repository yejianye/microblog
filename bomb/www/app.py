
#!/usr/bin/env python
import os
from flask import Flask

from bomb.www import api as www_api
from bomb.www.base import load_views

def create_app():
    app = Flask(__name__)
    app.config.from_object('bomb.www.conf.{}'.format(os.environ.get('ENV_NAME', 'dev')))
    app.debug = app.config['DEBUG']
    load_views(app, www_api)
    return app

api_site = create_app()
