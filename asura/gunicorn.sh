#!/bin/bash
gunicorn -k gevent -w 3 --bind 0.0.0.0:7431 asura.app:default_app
