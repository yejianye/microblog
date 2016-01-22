#!/usr/bin/env python
import os
from flask import Flask
from pprint import pprint

from asura.www import api as www_api
from asura.extensions import db
from asura.www.base import load_views
from mbutils import cache

def create_app():
    app = Flask(__name__)
    app.config.from_object('asura.conf.{}'.format(os.environ.get('ENV_NAME', 'dev')))
    app.debug = app.config['DEBUG']
    load_views(app, www_api)
    db.init_app(app)
    cache.init(app.config['REDIS_HOST'], app.config['REDIS_PORT'])
    return app

default_app = create_app()
