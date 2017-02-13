# config.py

import json
import os
import pathlib

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
    lost_pub = '''MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCCbRAw9NYhb5NUpEtZjxpFibRh
			9X5xXbp5p7Z0eIarE3RFH6fA7xn7fMINN6vGIxyd370areElYUqZgxelXnzs80gO
			FMdrbND/bVDEzgxwnUctAiOY6qrqww90CkJE1VhIZQhxQpFLEMQvXOTN5uBQjF2D
			eAke9RjVacpKaNj26wIDAQAB'''
    lost_priv  = '''MIICXQIBAAKBgQCCbRAw9NYhb5NUpEtZjxpFibRh9X5xXbp5p7Z0eIarE3RFH6fA
			7xn7fMINN6vGIxyd370areElYUqZgxelXnzs80gOFMdrbND/bVDEzgxwnUctAiOY
			6qrqww90CkJE1VhIZQhxQpFLEMQvXOTN5uBQjF2DeAke9RjVacpKaNj26wIDAQAB
			AoGAUqY+Tme4kfOcj1SVkylF4q8CqdjhyYE1vAX1bxU5cYugcHVA3tglxOIoLiwL
			JEH3zmuL8C4jsIZYubMC9v5LdwoXpnyGRl4LDBB+Iod6nF/mbW3e/N9Glop8gjf+
			Qcv+TIKWw9FvByK7aJDaOkOn3anfHCD5lJCFsaXGnZdjTlECQQDTkQgwE3Yu2vAP
			hyVjSCZNamCzNZGZQ5b1Id8PzwV0K6HvdaseeawTloeQbB4ysjqcJCRSWcVUCZ97
			3/8km4v3AkEAndF57XOSyQFA6syM85GCpldu5NdNfWUSh/IEDfBCXIz4HgvAHHSs
			LpANlKfcQm/jAt9M053I8SSytW/gZC1nrQJBAIPGbgcj2BTPIX9KeisgoVrOy3RU
			BWAlDT2Z30oFdCwrkS2JaRAOUPPSapW2Agkpof/nMwhoCdSSOdf6aPzwNXkCQCD5
			6l5BbgRuLKBjSXiDiSc00ckja9+txOd/HHXFJDiuhBHTJrtLbcb09sF/KbkAJBEv
			k6AMMjahEm5zCBImoqkCQQCr2dol/0ALuYOiX9HjrdUzYimV8dK2pRun9st7kG61
			om7WCcOAgUeF9evc07QrmK84bYECq+cIjZRPD0Ww89Cs'''


