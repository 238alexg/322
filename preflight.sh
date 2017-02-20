#!/usr/bin/bash

cd sql

psql $1 -f create_tables.sql
