#!/usr/bin/bash

# Go into sql folder, create tables, then return to current folder
cd sql
psql $1 -f create_tables.sql
cd ..

# Copies all files to the /wsgi directory
cp -R src/* $HOME/wsgi

# Comment out before submission!
# Restarts server
#apachectl restart
#python3 ../../wsgi/app.py $1
