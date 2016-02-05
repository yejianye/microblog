#!/bin/bash
gunicorn -k gevent -w 3 --bind 0.0.0.0:7431 bomb.www.app:api_site
