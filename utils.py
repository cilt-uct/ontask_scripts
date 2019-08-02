import csv
import pandas

from collections import OrderedDict
from calls.ontask_login_calls import *
from transform.transform_memberships_data import *
from transform.transform_gradebook_data import *


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


def create_gradebook_csv(gradebook_data, source):
    try:
        cols = list(map(lambda x: "GB " + x['itemName'], gradebook_data))
        cols = ordered_unique_list(cols)

        # get all userIds, set to filter duplicates, list to maintain order.
        row_headers_userid = list(set(map(lambda x: x['userId'], gradebook_data)))
        rows = create_table(gradebook_data, row_headers_userid)
        userid_usereid_dict = get_userid_usereid_dict()
        row_headers_usereid = list(map(lambda x: userid_usereid_dict[x], row_headers_userid))

        data_frame = pandas.DataFrame(rows, columns=cols, index=row_headers_usereid)
        data_frame.to_csv(CSV_PATH + source + ".csv", index=True, index_label="userId", header=True)
        return True
    except Exception as e:
        logging.error('Something went wrong during the creation of a CSV via a data-frame:' + str(e))

    return False


def get_userid_usereid_dict():
    userid_usereid_dict = {}

    with open(CSV_PATH+'Vula_Memberships.csv', newline='') as csv_file:

        memberships = csv.reader(csv_file, delimiter=',', quotechar='"')
        next(memberships)

        for row in memberships:
            userid_usereid_dict[row[8]] = row[6]

    return userid_usereid_dict
