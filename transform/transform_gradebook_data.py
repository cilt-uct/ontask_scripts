import csv
import pandas

from config.logging_config import *


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
        data_frame.to_csv(CSV_PATH + source + ".csv", index=True, index_label="UserEid", header=True)
        return True
    except Exception as e:
        logging.error('Something went wrong during the creation of a CSV via a data-frame:' + str(e))

    return False


def get_userid_usereid_dict():
    userid_usereid_dict = {}

    with open(CSV_PATH+'Vula_Memberships.csv', newline='') as csv_file:

        memberships = csv.reader(csv_file, delimiter=',', quotechar='"')
        headers = next(memberships)
        usereid = headers.index('userEid')
        userid = headers.index('userId')

        for row in memberships:
            userid_usereid_dict[row[userid]] = row[usereid]

    return userid_usereid_dict


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