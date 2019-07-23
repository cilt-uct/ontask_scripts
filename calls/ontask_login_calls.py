import json
import requests

from config.logging_config import *
from requests import HTTPError


def ontask_login():
    url = ONTASK['url'] + 'auth/local/'
    payload = {'email': ONTASK['email'], 'password': ONTASK['password']}
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload)

    try:
        r = requests.post(url, data=data, headers=headers)
        r.raise_for_status()
        login_response = json.loads(r.text)
        return login_response['token']
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(repr(status_code) + ": Failed to log into OnTask.")


def ontask_login_as_owner(owner):
    url = ONTASK['url'] + 'auth/impersonate/'
    payload = {'email': owner}
    headers = {'Content-Type': 'application/json', 'Authorization': "Token " + ontask_login()}
    data = json.dumps(payload)

    try:
        r = requests.post(url, data=data, headers=headers)
        r.raise_for_status()
        login_response = json.loads(r.text)
        return login_response['token']
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(repr(status_code) + ": Failed to log into OnTask.")
