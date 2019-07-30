from calls.ontask_data_calls import *
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
    for container in containers:
        logging.info("Import for container: " + container['code'] + " has started.")

        if container['description'] is None:
            logging.warning("Container: " + container['code'] + " description does not contain site ID.")
            continue

        session = vula_login()
        exists = check_if_site_exists(container['description'], session)
        if not exists:
            logging.warning("Container: " + container['code'] + " site ID does not exist in Vula.")
            continue

        data_sources = json.loads(get_all_data_sources(container['owner']))
        data_sources = list(filter(lambda x: x['container'] == container['id'], data_sources))
        import_site_data(data_sources, container, session)
        logging.info("Import for container: " + container['code'] + " complete.")


def import_site_data(data_sources, container, session):
    auto_import_data_sources = ['Vula_Memberships', 'Vula_Gradebook']

    data_source_check = do_all_data_sources_exist(data_sources, auto_import_data_sources)

    # If containers do not have data sources or one of the auto_import_data_sources are not in data_sources
    #  -> create memberships and gradebook data-sources
    if not data_sources or not data_source_check:
        url = ONTASK['url'] + 'datasource/'
        create_data_sources(container, url, auto_import_data_sources, session)

    # If container has data sources, check if they are in the auto_import_data_sources, if not -> skip
    # if in the list then update data source
    for data_source in data_sources:
        if data_source['name'] not in auto_import_data_sources:
            continue

        url = ONTASK['url'] + 'datasource/' + data_source['id'] + '/'
        update_data_sources(container, url, data_source, session)


def create_data_sources(container, url, sources, session):
    update_memberships(container, url, sources[0], session, True)
    update_gradebook(container, url, sources[1], session, True)


def update_data_sources(container, url, source, session):
    data_source_name = source['name']
    if data_source_name == 'Vula_Memberships':
        update_memberships(container, url, data_source_name, session, False)
    elif data_source_name == 'Vula':
        update_gradebook(container, url, data_source_name, session, False)


def update_memberships(container, url, source, session, create):
    site_members = get_site_memberships(container['description'], session)
    if site_members:
        site_members = site_members['membership_collection']
        if create_csv(site_members, source + ".csv"):
            import_csv(container, url, source, create)


def update_gradebook(container, url, source, session, create):
    gradebook_data = get_gradebook_data(container['description'], session)
    if gradebook_data:
        gradebook_data = gradebook_data['assignments']
        if transform_data(gradebook_data, source):
            import_csv(container, url, source, create)


update_container_data()
