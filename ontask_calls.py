import json

from utils import *
from vula_calls import *


def ontask_login():
    url = ONTASK['url'] + 'auth/local/'
    payload = {'email': ONTASK['email'], 'password': ONTASK['password']}
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload)

    r = requests.post(url, data=data, verify=False, headers=headers)
    return r.text


def get_all_containers(token):
    url = ONTASK['url'] + 'administration/containers/'
    headers = {'Authorization': "Token " + token}

    r = requests.get(url, verify=False, headers=headers)
    return r.text


def get_all_data_sources(owner, token):
    url = ONTASK['url'] + 'datasource/'
    payload = {'owner': owner}
    headers = {'Authorization': "Token " + token}

    r = requests.get(url, data=payload, verify=False, headers=headers)
    return r.text


def create_data_sources(container, url, token, sources):
    session = vula_login()
    site_members = json.loads(get_site_memberships(container['description'], session))['membership_collection']
    gradebook_data = json.loads(get_gradebook_data(container['description'], session))['assignments']

    create_csv(site_members, sources[0] + ".csv")
    create_csv(gradebook_data, sources[1] + ".csv")

    for source in sources:

        files = {'file': open(source+'.csv', 'rb')}
        payload = {
            'name': source,
            'container': container['id'],
            'payload': '{"connection":{"dbType":"csvTextFile","files":[{"name":"test_csv.csv","delimiter":","}]},'
                       '"name":"Test"}',
        }
        headers = {'Authorization': "Token " + token}

        r = requests.post(url, data=payload, files=files, verify=False, headers=headers)
        print(r.text)


def update_data_sources(container, url, token, source):
    session = vula_login()

    if source is 'Vula_Memberships':
        site_members = json.loads(get_site_memberships(container['description'], session))['membership_collection']
        create_csv(site_members, source + ".csv")
    elif source is 'Vula_Gradebook':
        gradebook_data = json.loads(get_gradebook_data(container['description'], session))['assignments']
        create_csv(gradebook_data, source + ".csv")

    files = {'file': open(source+'.csv', 'rb')}
    payload = {
        'name': source,
        'container': container['id'],
        'payload': '{"connection":{"dbType":"csvTextFile","files":[{"name":"test_csv.csv","delimiter":","}]},'
                   '"name":"Test"}',
    }
    headers = {'Authorization': "Token " + token}

    r = requests.patch(url, data=payload, files=files, verify=False, headers=headers)

    print(r.text)
