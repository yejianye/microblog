#!/usr/bin/env python
import os
from flask import Flask

import mbref.www.api
from mbref.extensions import db
from mbref.www.base import load_views

def create_app():
    app = Flask(__name__)
    app.config.from_object('mbref.conf.{}'.format(os.environ.get('ENV_NAME', 'dev')))
    app.debug = app.config['DEBUG']
    load_views(app, mbref.www.api)
    db.init_app(app)
    return app

default_app = create_app()
