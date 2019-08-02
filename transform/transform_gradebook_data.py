from config.logging_config import *


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