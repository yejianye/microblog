#!/usr/bin/env python
import os

from webrpc.server import Server
from mbutils import cache
from bomb.mbsrv.models.base import db
from bomb.mbsrv.logic import MicroBlogLogic

def create_app():
    app = Server('microblog', MicroBlogLogic())
    app.config.from_object('bomb.mbsrv.conf.{}'.format(os.environ.get('ENV_NAME', 'dev')))
    app.debug = app.config['DEBUG']
    db.init_app(app)
    cache.init(app.config['REDIS_HOST'], app.config['REDIS_PORT'])
    return app

mbsrv_site = create_app()
