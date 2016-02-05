#!/bin/bash
gunicorn -k gevent -w 3 --bind 0.0.0.0:7777 bomb.mbsrv.app:mbsrv_site
