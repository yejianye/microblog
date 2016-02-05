#!/usr/bin/env python

from bomb.mbsrv.app import mbsrv_site
from bomb.mbsrv.models.base import db

with mbsrv_site.app_context():
    db.drop_all()
    db.create_all()
