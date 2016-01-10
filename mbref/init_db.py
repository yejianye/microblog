#!/usr/bin/env python

from mbref.app import db

# Register models
import mbref.models.user
import mbref.models.feed

db.drop_all()
db.create_all()
