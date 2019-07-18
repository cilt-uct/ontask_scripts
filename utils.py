import csv


def create_csv(data, file_name):
    output_file = open(file_name, 'w')

    output = csv.writer(output_file)
    output.writerow(data[0].keys())
    for row in data:
        output.writerow(row.values())


def do_all_data_sources_exist(existing, required):

    if len(existing) < len(required):
        return False

    existing = list(map(lambda x: x['name'], existing))

    if set(required).issubset(set(existing)):
        return True
    else:
        return False