from constants import ACTIVE_NOTARY_LIST_URL
from requests import request, Response
from sys import exit
from hashlib import sha1

ACTIVE_NOTARY_LIST_URL: str = 'https://notary.cdn.sos.ca.gov/export/active-notary.zip'

def get_active_notary_archive()->bytes:

    r: Response = request("GET", ACTIVE_NOTARY_LIST_URL)

    # Exit if Status Code != 200
    if r.status_code != 200:
        print(f"[ERROR] Status Code: {r.status_code} Error Message: {r.content}")
        exit(1)

    return r.content

