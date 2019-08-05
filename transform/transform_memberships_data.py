import csv

from config.logging_config import *
from collections import OrderedDict


def create_memberships_csv(data, file_name):
    try:
        output_file = open(CSV_PATH + file_name, 'w')
        output = csv.writer(output_file)
        output.writerow(header(data[0]))

        for row in data:
            delete_unwanted_keys(row)
            update_student_number(row)
            update_name(row)
            sorted_row = OrderedDict(sorted(row.items()))
            output.writerow(sorted_row.values())

        return True
    except Exception as e:
        logging.error('Something went wrong during the creation of a CSV: ' + str(e))

    return False


def delete_unwanted_keys(row):
    row.pop('locationReference', None)
    row.pop('lastLoginTime', None)
    row.pop('entityReference', None)
    row.pop('entityId', None)
    row.pop('id', None)
    row.pop('entityURL', None)
    row.pop('siteType', None)
    row.pop('userDisplayId', None)
    row.pop('entityTitle', None)
    return row


def update_student_number(row):
    try:
        row['userEid'] = row['userEid'].upper()
        return row
    except Exception as e:
        logging.error("Something went wrong during the capitalisation of the student number: " + str(e))
        return row


def update_name(row):
    try:
        full_name = row['userSortName'].replace(" ", "").split(",")
        row['firstname'] = full_name[1]
        row['lastname'] = full_name[0]
        return row
    except Exception as e:
        logging.error("Something went wrong during the separation of firstname and lastname : " + str(e))
        return row


def header(first_row):
    headers = delete_unwanted_keys(first_row).keys()
    headers_list = list(headers)
    headers_list.extend(['firstname', 'lastname'])
    headers_list.sort()
    return headers_list
