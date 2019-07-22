from ontask_calls import *
from config.logging_config import *


def update_container_data():
    logging.info("____________________________________________________________________________________________________")
    logging.info("Start of import session.")

    login_response = json.loads(ontask_login())
    token = login_response['token']

    containers = json.loads(get_all_containers(token))

    logging.info("Fetched " + repr(len(containers)) + " containers successfully.")

    # foreach container, get all the data sources linked to that container and update/create them
    for container in containers:
        data_sources = json.loads(get_all_data_sources(container['owner'], token))
        import_site_data(data_sources, container, token)


def import_site_data(data_sources, container, token):
    auto_import_data_sources = ['Vula_Memberships', 'Vula_Gradebook']

    data_source_check = do_all_data_sources_exist(data_sources, auto_import_data_sources)

    # If containers do not have data sources or one of the auto_import_data_sources are not in data_sources
    #  -> create memberships and gradebook data-sources
    if not data_sources or not data_source_check:
        url = ONTASK['url'] + 'datasource/'
        create_data_sources(container, url, token, auto_import_data_sources)

    # If container has data sources, check if they are in the auto_import_data_sources, if not -> skip
    # if in the list then update data source
    for data_source in data_sources:
        if data_source['name'] not in auto_import_data_sources:
            continue

        url = ONTASK['url'] + 'datasource/' + data_source['id'] + '/'
        r = update_data_sources(container, url, token, data_source)
        if r is not None:
            logging.info(
                "Updated container: " + container['code'] + " data-source: " + data_source['name'] + ", successfully.")

    logging.info("Import session completed.")
    logging.info("____________________________________________________________________________________________________")


update_container_data()
