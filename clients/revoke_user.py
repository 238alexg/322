# Alex Geoffrey
# CIS 322
# revoke_user.py

# Modified from Andrew Hampton's code example on Piazza.com

import sys
import json
import datetime

from urllib.request import Request, urlopen
from urllib.parse import urlencode

def main():
    # Check CLI args
    if (len(sys.argv) < 3):
        print("Correct usage: python3 revoke_user.py <url> <username>")
        return

    args = dict()
    args['username'] = sys.argv[2]

    # Set up data
    data = urlencode(args)

    # Make the request
    req = Request(sys.argv[1] + "revoke_user", data.encode('ascii'), method='POST')

    # Get webserver response
    res = urlopen(req)
    print("Call returned: %s"% res.read())

if (__name__  == '__main__'):
    main()



