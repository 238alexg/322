# Config.py
# Created on 2/19/17 by Alex Geoffrey
# For CIS322 at the University of Oregon

# Adopted from Professor Ellsworth's config.py

import json
import os
import pathlib

# Set up json file pathway
cpath = pathlib.Path(os.path.realpath(__file__)).parent.joinpath('lost_config.json')

# Open config JSON
with cpath.open() as conf:
    # Load in JSON
    c = json.load(conf)

    # DB info
    dbname = c['database']['dbname']
    dbhost = c['database']['dbhost']
    dbport = c['database']['dbport']
    
    # Secret key (for sessions)
    secret_key = c['crypto']['lost_priv']

    print (dbname, dbhost, dbport)

