import csv
import pandas

from collections import OrderedDict
from calls.ontask_login_calls import *
from config.logging_config import *


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


def create_csv(data, file_name):
    try:
        output_file = open(CSV_PATH + file_name, 'w')

        output = csv.writer(output_file)

        first_row = data[0]
        headers = delete_unwanted_keys(first_row).keys()
        headers_list = list(headers)
        headers_list.extend(['firstname', 'lastname'])
        headers_list.sort()
        print(headers_list)
        output.writerow(headers_list)
        for row in data:
            delete_unwanted_keys(row)
            update_student_number(row)
            update_name(row)
            sorted_row = list(row.items())
            sorted_row.sort()
            sorted_dict = OrderedDict(sorted_row)
            print(sorted_dict)
            output.writerow(sorted_dict.values())
        return True
    except Exception as e:
        logging.error('Something went wrong during the creation of a CSV: ' + str(e))

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


def transform_data(gradebook_data, source):
    try:
        cols = list(map(lambda x: "GB " + x['itemName'], gradebook_data))
        cols = ordered_unique_list(cols)
        row_headers = set(map(lambda x: x['userId'], gradebook_data))
        rows = create_table(gradebook_data, row_headers)
        data_frame = pandas.DataFrame(rows, columns=cols, index=row_headers)
        data_frame.to_csv(CSV_PATH + source + ".csv", index=True, index_label="userId", header=True)
        return True
    except Exception as e:
        logging.error('Something went wrong during the creation of a CSV via a data-frame:' + e.message)

    return False


def create_table(gradebook_data, row_headers):
    rows = []
    if len(gradebook_data) == 0 or len(row_headers) == 0:
        logging.error("Gradebook or row headers are empty")
        return rows

    for row in row_headers:
        grades = []
        for grade in gradebook_data:
            if row == grade['userId']:
                grades.append(grade['grade'])

        rows.append(grades)
    return rows


def ordered_unique_list(columns):
    seen = set()
    seen_add = seen.add
    return [x for x in columns if not (x in seen or seen_add(x))]
