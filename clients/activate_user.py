# Alex Geoffrey
# CIS 322
# activate_user.py

# Modified from Andrew Hampton's code example on Piazza.com

import sys
import json
import datetime

from urllib.request import Request, urlopen
from urllib.parse import urlencode

def main():
    # Check CLI args
    if (len(sys.argv) < 5):
        print("Correct usage: python3 activate_user.py <url> <username> <password> <role>")
        return

    args = dict()
    args['username'] = sys.argv[2]
    args['password'] = sys.argv[3]
    args['role'] = sys.argv[4]

    # Set up data
    data = urlencode(args)

    # Make the request
    req = Request(sys.argv[1] + "activate_user", data.encode('ascii'), method='POST')

    # Get webserver response
    res = urlopen(req)

    print("Call returned: %s"% res.read())

if (__name__  == '__main__'):
    main()



