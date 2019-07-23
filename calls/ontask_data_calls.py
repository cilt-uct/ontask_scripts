import json

from utils import *
from calls.vula_calls import *


def get_all_containers():
    url = ONTASK['url'] + 'administration/containers/'
    headers = {'Authorization': "Token " + ontask_login()}

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(repr(status_code) + ": Failed to get all containers from OnTask.")


def get_all_data_sources(owner):
    url = ONTASK['url'] + 'datasource/'
    payload = {'owner': owner}
    headers = {'Authorization': "Token " + is_container_owner_admin(owner)}

    try:
        r = requests.get(url, data=payload, headers=headers)
        r.raise_for_status()
        return r.text
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(repr(status_code) + ": Failed to get all data sources from OnTask. Check container ID.")


def create_data_sources(container, url, sources):
    site_members = get_site_memberships(container['description'])['membership_collection']
    create_csv(site_members, sources[0] + ".csv")

    gradebook_data = get_gradebook_data(container['description'])

    if not gradebook_data:
        del sources[-1]
        pass
    else:
        gradebook_data = gradebook_data['assignments']
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
        headers = {'Authorization': "Token " + is_container_owner_admin(container['owner'])}

        try:
            r = requests.post(url, data=payload, files=files, headers=headers)
            r.raise_for_status()
            logging.info("Successfully created datasource: " + source + " for container: " + container['code'])
        except HTTPError as e:
            status_code = e.response.status_code
            logging.error(
                repr(status_code) + ": Failed to create data-sources OnTask. Container: " +
                container['code'] + " on OnTask. " + e.response.text)


def update_data_sources(container, url, source):
    data_source_name = source['name']
    if data_source_name == 'Vula_Memberships':
        site_members = get_site_memberships(container['description'])['membership_collection']
        create_csv(site_members, data_source_name + ".csv")
    elif data_source_name == 'Vula_Gradebook':
        gradebook_data = get_gradebook_data(container['description'])['assignments']
        create_csv(gradebook_data, data_source_name + ".csv")

    files = {'file': open(CSV_PATH + data_source_name + '.csv', 'rb')}
    payload = {
        'name': data_source_name,
        'container': container['id'],
        'payload': '{"connection":{"dbType":"csvTextFile","files":[{"name":"'
                   + data_source_name + '.csv","delimiter":","}]},"name":"Test"}',
    }
    headers = {'Authorization': "Token " + is_container_owner_admin(container['owner'])}

    try:
        r = requests.patch(url, data=payload, files=files, headers=headers)
        r.raise_for_status()
        return r
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(
            repr(status_code) + ": Failed to update data for container: " +
            container['code'] + " data-source: " + data_source_name + " on OnTask. " + e.response.text)
