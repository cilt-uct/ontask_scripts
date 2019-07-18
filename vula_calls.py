import requests

from config import *


def vula_login():
    url = VULA['url'] + 'direct/session'
    body = {'_username': VULA['username'], '_password': VULA['password']}
    headers = {'Accept': "application/json",'Cache-Control': "no-cache"}

    r = requests.post(url, data=body, headers=headers)
    return r.text


def get_site_memberships(site_id, session):
    url = VULA['url'] + 'direct/site/' + site_id + '/memberships?_validateSession=true&sakai.session=' + session
    headers = {'Accept': 'application/json','Cache-Control': "no-cache"}

    r = requests.get(url, headers=headers)
    return r.text


def get_gradebook_data(site_id, session):
    url = VULA['url'] + 'direct/gradebook/site/' + site_id + '?_validateSession=true&sakai.session=' + session
    headers = {'Accept': 'application/json','Cache-Control': "no-cache"}

    r = requests.get(url, headers=headers)
    return r.text