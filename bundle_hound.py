#!/usr/bin/env python3

 

import certifi

import json

import pprint

import sys

import urllib3

 

from pprint import PrettyPrinter

from urllib.request import urlopen

 

def main():

    """

    Validates bundles' metadata by checking if titles, descriptions,

    and tags are empty and reports results.

    """

 

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

    req = http.request(

            'GET',

            "https://download.clearlinux.org/releases/current/assets/bundles/bundles.json",

            timeout=10.0)

 

    if req.status != 200:

        print(f'[Error] Connection: {req.status} {req.reason}')

        sys.exit(2)

 

    json_data = json.loads(req.data.decode('utf-8'))

    bundles = json_data["bundles"]

 

    missing = [ b['title'] for b in bundles if not b['description'] or not b['tags'] ]

    if missing:

        print("Bundles missing metadata:")

        pprint.pprint(f"{missing}", width=1)

        print("")

 

    no_title = [ b for b in bundles if not b['title'] ]

    if no_title:

        print("Bundles missing title:")

        pprint.pprint(no_title)

 

    if missing or no_title:

        sys.exit(1)

 

if __name__ == "__main__":

    main()