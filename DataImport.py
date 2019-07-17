import requests, json, sys, csv
from config import *


def login():
    url = ONTASK['url']+'auth/local/'

    payload = {
        'email': ONTASK['email'],
        'password': ONTASK['password']
    }

    headers = {
        'Content-Type': 'application/json'
    }

    data = json.dumps(payload)

    r = requests.post(url, data=data, verify=False, headers=headers)
    return r.text


def get_all_containers(token):
    url = ONTASK['url']+'administration/containers/'

    r = requests.get(url, verify=False, headers=get_header(token))
    return r.text


def create_data_sources(container, url, token):
    site_members = json.loads(get_site_memberships(container['description']))['membership_collection']
    create_csv(site_members, "memberships.csv")

    files = {'file': open('memberships.csv', 'rb')}
    payload = get_payload('membership', container['id'])

    r = requests.post(url, data=payload, files=files, verify=False, headers=get_header(token))
    print(r.text)


def update_container_data():
    login_response = json.loads(login())
    token = login_response['token']

    containers = json.loads(get_all_containers(token))

    for container in containers:

        create_url = ONTASK['url']+'datasource/'

        data_sources = json.loads(get_all_data_sources(container['owner'], create_url, token))

        if not data_sources:
            create_data_sources(container, create_url, token)

        for data_source in data_sources:
            patch_url = ONTASK['url']+'datasource/' + data_source['id'] + '/'

            site_members = json.loads(get_site_memberships(container['description']))['membership_collection']
            create_csv(site_members, "memberships.csv")

            files = {'file': open('memberships.csv', 'rb')}
            payload = get_payload('membership', container['id'])

            r = requests.patch(patch_url, data=payload, files=files, verify=False, headers=get_header(token))

            print(r.text)


def get_all_data_sources(owner, url, token):
    payload = {
        'owner': owner
    }

    r = requests.get(url, data=payload, verify=False, headers=get_header(token))

    return r.text

def create_csv(data, file_name):

    output_file = open(file_name, 'w')  # load csv file

    output = csv.writer(output_file)  # create a csv.write
    output.writerow(data[0].keys())  # header row
    for row in data:
        output.writerow(row.values())  # values row


def vula_login():
    url = VULA['url']+'direct/session'

    body = {
        '_username': VULA['username'],
        '_password': VULA['password']
    }

    headers = {
        'Accept': "application/json",
        'Cache-Control': "no-cache"
    }

    r = requests.post(url, data=body, headers=headers)
    return r.text


def get_site_memberships(siteId):
    session = vula_login()
    url = VULA['url']+'direct/site/'+siteId+'/memberships?_validateSession=true&sakai.session='+session

    headers = {
        'Accept': 'application/json',
        'Cache-Control': "no-cache"
    }

    r = requests.get(url, headers=headers)
    return r.text


def get_payload(name, container):
    payload = {
        'name': name,
        'container': container,
        'payload': '{"connection":{"dbType":"csvTextFile","files":[{"name":"test_csv.csv","delimiter":","}]},'
                   '"name":"Test"}',
    }

    return payload


def get_header(token):
    headers = {
        'Authorization': "Token " + token
    }

    return headers


update_container_data()
