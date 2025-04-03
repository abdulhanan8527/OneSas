#!/bin/bash
# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles
# Copy static files from OneSas_app to staticfiles
cp -r OneSas_app/static/* staticfiles/
# Run collectstatic
python manage.py collectstatic --noinput