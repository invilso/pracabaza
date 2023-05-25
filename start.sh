#!/bin/bash
cd /var/www/website/
source env/bin/activate
gunicorn -c /var/www/website/gunicorn_config.py website.wsgi
