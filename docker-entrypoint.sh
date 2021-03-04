#!/bin/sh

gunicorn -c etc/gunicorn.py manage:app