# config.py

import json
import os
import pathlib
from Crypto.PublicKey import RSA

# Get path for json file
cpath = pathlib.Path(os.path.realpath(__file__)).parent.joinpath('lost_config.json')

# Open config JSON
with cpath.open() as conf:

	# Load in JSON file
    c = json.load(conf)

    # DB info
    dbname = c['database']['dbname']
    dbhost = c['database']['dbhost']
    dbport = c['database']['dbport']

    # Keys
    lost_pub  = RSA.generate(2048)
    lost_pub  = lost_pub.exportKey(pkcs=8)