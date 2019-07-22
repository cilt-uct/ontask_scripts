import json

from utils import *
from vula_calls import *


def ontask_login():
    url = ONTASK['url'] + 'auth/local/'
    payload = {'email': ONTASK['email'], 'password': ONTASK['password']}
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload)

    try:
        r = requests.post(url, data=data, verify=False, headers=headers)
        r.raise_for_status()
        return r.text
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(repr(status_code) + ": Failed to log into OnTask.")


def get_all_containers(token):
    url = ONTASK['url'] + 'administration/containers/'
    headers = {'Authorization': "Token " + token}

    try:
        r = requests.get(url, verify=False, headers=headers)
        r.raise_for_status()
        return r.text
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(repr(status_code) + ": Failed to get all containers from OnTask.")


def get_all_data_sources(owner, token):
    url = ONTASK['url'] + 'datasource/'
    payload = {'owner': owner}
    headers = {'Authorization': "Token " + token}

    try:
        r = requests.get(url, data=payload, verify=False, headers=headers)
        r.raise_for_status()
        return r.text
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(repr(status_code) + ": Failed to get all data sources from OnTask.")


def create_data_sources(container, url, token, sources):
    session = vula_login()
    site_members = json.loads(get_site_memberships(container['description'], session))['membership_collection']
    gradebook_data = json.loads(get_gradebook_data(container['description'], session))['assignments']

    create_csv(site_members, sources[0] + ".csv")
    create_csv(gradebook_data, sources[1] + ".csv")

    for source in sources:

        files = {'file': open(CSV_PATH + source + '.csv', 'rb')}
        payload = {
            'name': source,
            'container': container['id'],
            'payload': '{"connection":{"dbType":"csvTextFile","files":[{"name":"'
                       + source + '.csv","delimiter":","}]},'
                                  '"name":"Test"}',
        }
        headers = {'Authorization': "Token " + token}

        try:
            r = requests.post(url, data=payload, files=files, verify=False, headers=headers)
            r.raise_for_status()
            logging.info("Successfully created datasource: " + source + " for container: " + container['code'])
        except HTTPError as e:
            status_code = e.response.status_code
            logging.error(
                repr(status_code) + ": Failed to create data-sources OnTask. Container: " +
                container['code'] + " on OnTask. " + e.response.text)


def update_data_sources(container, url, token, source):
    session = vula_login()
    data_source_name = source['name']
    if data_source_name == 'Vula_Memberships':
        site_members = json.loads(get_site_memberships(container['description'], session))['membership_collection']
        create_csv(site_members, data_source_name + ".csv")
    elif data_source_name == 'Vula_Gradebook':
        gradebook_data = json.loads(get_gradebook_data(container['description'], session))['assignments']
        create_csv(gradebook_data, data_source_name + ".csv")

    files = {'file': open(CSV_PATH + data_source_name + '.csv', 'rb')}
    payload = {
        'name': data_source_name,
        'container': container['id'],
        'payload': '{"connection":{"dbType":"csvTextFile","files":[{"name":"'
                   + data_source_name + '.csv","delimiter":","}]},"name":"Test"}',
    }
    headers = {'Authorization': "Token " + token}

    try:
        r = requests.patch(url, data=payload, files=files, verify=False, headers=headers)
        r.raise_for_status()
        return r
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(
            repr(status_code) + ": Failed to update data for container: " +
            container['code'] + " data-source: " + data_source_name + " on OnTask. " + e.response.text)
