#!/usr/bin/env python
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('mbref.conf.{}'.format(os.environ.get('ENV_NAME', 'dev')))
db = SQLAlchemy(app)

