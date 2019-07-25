import csv

from calls.ontask_login_calls import *
from config.logging_config import *


def create_csv(data, file_name):
    try:
        output_file = open(CSV_PATH + file_name, 'w')

        output = csv.writer(output_file)
        output.writerow(data[0].keys())
        for row in data:
            output.writerow(row.values())
        return True
    except Exception as e:
        logging.error('Something went wrong during the creation of a CSV:' + e.message)

    return False


def do_all_data_sources_exist(existing, required):
    if len(existing) < len(required):
        return False

    existing = list(map(lambda x: x['name'], existing))

    if set(required).issubset(set(existing)):
        return True
    else:
        return False


def is_container_owner_admin(owner):
    if owner != ONTASK['email']:
        return ontask_login_as_owner(owner)
    else:
        return ontask_login()
