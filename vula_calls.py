import requests

from requests import HTTPError
from config.config import *
from config.logging_config import *


def vula_login():
    url = VULA['url'] + 'direct/session'
    body = {'_username': VULA['username'], '_password': VULA['password']}
    headers = {'Accept': "application/json",'Cache-Control': "no-cache"}

    try:
        r = requests.post(url, data=body, headers=headers)
        r.raise_for_status()
        return r.text
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(repr(status_code) + ": Failed to log into Vula.")


def get_site_memberships(site_id, session):
    url = VULA['url'] + 'direct/site/' + site_id + '/memberships?_validateSession=true&sakai.session=' + session
    headers = {'Accept': 'application/json','Cache-Control': "no-cache"}

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(repr(status_code) + ": Failed to get site memberships from Vula.")


def get_gradebook_data(site_id, session):
    url = VULA['url'] + 'direct/gradebook/site/' + site_id + '?_validateSession=true&sakai.session=' + session
    headers = {'Accept': 'application/json','Cache-Control': "no-cache"}

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(repr(status_code) + ": Failed to get gradebook data from Vula.")
