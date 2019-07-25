import requests
import json

from requests import HTTPError
from config.logging_config import *


def vula_login():
    url = VULA['url'] + 'direct/session'
    body = {'_username': VULA['username'], '_password': VULA['password']}
    headers = {'Accept': "application/json", 'Cache-Control': "no-cache"}

    try:
        session = requests.Session()
        r = session.post(url, data=body, headers=headers)
        r.raise_for_status()
        return session
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(repr(status_code) + ": Failed to log into Vula.")


def check_if_site_exists(site_id, session):
    url = VULA['url'] + 'direct/site/' + site_id + '/exists'

    try:
        r = session.get(url)
        r.raise_for_status()
        return True
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(repr(status_code) + ": Site: " + site_id + " does not exist in Vula.")
        return False


def get_site_memberships(site_id, session):
    url = VULA['url'] + 'direct/site/' + site_id + '/memberships'
    headers = {'Accept': 'application/json', 'Cache-Control': "no-cache"}

    try:
        r = session.get(url, headers=headers)
        r.raise_for_status()
        return json.loads(r.text)
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(repr(status_code) + ": Failed to get site memberships for site: " + site_id + " from Vula.")
        return {}


def get_gradebook_data(site_id, session):
    url = VULA['url'] + 'direct/gradebook/site/' + site_id
    headers = {'Accept': 'application/json', 'Cache-Control': "no-cache"}

    try:
        r = session.get(url, headers=headers)
        r.raise_for_status()
        return json.loads(r.text)
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(repr(status_code) + ": Failed to get gradebook data for site: " + site_id + " from Vula.")
        return {}
