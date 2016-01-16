#!/usr/bin/env python

from mbref.app import db, create_app

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
