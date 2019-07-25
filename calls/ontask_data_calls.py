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


def import_csv(container, url, source, create):
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
        if create:
            r = requests.post(url, data=payload, files=files, headers=headers)
            message = "Successfully created data-source: " + source + " for container: " + container['code']
        else:
            r = requests.patch(url, data=payload, files=files, headers=headers)
            message = "Successfully updated data-source: " + source + " for container: " + container['code']

        r.raise_for_status()
        logging.info(message)
    except HTTPError as e:
        status_code = e.response.status_code
        logging.error(
            repr(status_code) + ": Failed to create data-sources OnTask. Container: " +
            container['code'] + " on OnTask. " + e.response.text)
