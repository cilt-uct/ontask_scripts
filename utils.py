import csv
import pandas

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
