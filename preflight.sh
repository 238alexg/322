#!/usr/bin/bash

# Go into sql folder, create tables, then return to current folder
cd sql
psql $1 -f create_tables.sql
cd ..

cp -R src/* $HOME/wsgi


