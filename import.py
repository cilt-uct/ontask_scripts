from calls.ontask_calls import *
from config.logging_config import *


def update_container_data():
    logging.info("____________________________________________________________________________________________________")
    logging.info("Start of import session.")

    containers = json.loads(get_all_containers())
    logging.info("Fetched " + repr(len(containers)) + " containers successfully.")

    update_containers(containers)

    logging.info("Import session completed.")
    logging.info("____________________________________________________________________________________________________")


def update_containers(containers):
    # foreach container, get all the data sources linked to that container and update/create them
    for container in containers:
        logging.info("Import for container: " + container['code'] + " has started.")

        if container['description'] is None:
            logging.warning("Container: " + container['code'] + " does not have a description containing a Vula course "
                                                                "ID site and therefore no data updates.")
            continue

        exists = check_if_site_exists(container['description'])
        if not exists:
            logging.warning("Container: " + container['code'] + " does not have a description containing a Vula course "
                                                                "ID site and therefore no data updates.")
            continue

        data_sources = json.loads(get_all_data_sources(container['owner']))
        data_sources = list(filter(lambda x: x['container'] == container['id'], data_sources))
        import_site_data(data_sources, container)
        logging.info("Import for container: " + container['code'] + " complete.")


def import_site_data(data_sources, container):
    auto_import_data_sources = ['Vula_Memberships', 'Vula_Gradebook']

    data_source_check = do_all_data_sources_exist(data_sources, auto_import_data_sources)

    # If containers do not have data sources or one of the auto_import_data_sources are not in data_sources
    #  -> create memberships and gradebook data-sources
    if not data_sources or not data_source_check:
        url = ONTASK['url'] + 'datasource/'
        create_data_sources(container, url, auto_import_data_sources)

    # If container has data sources, check if they are in the auto_import_data_sources, if not -> skip
    # if in the list then update data source
    for data_source in data_sources:
        if data_source['name'] not in auto_import_data_sources:
            continue

        url = ONTASK['url'] + 'datasource/' + data_source['id'] + '/'
        r = update_data_sources(container, url, data_source)
        if r is not None:
            logging.info(
                "Updated container: " + container['code'] + " data-source: " + data_source['name'] + ", successfully.")


update_container_data()
