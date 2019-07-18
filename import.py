from ontask_calls import *


def update_container_data():
    login_response = json.loads(ontask_login())
    token = login_response['token']

    containers = json.loads(get_all_containers(token))

    for container in containers:
        data_sources = json.loads(get_all_data_sources(container['owner'], token))

        # import site membership data
        import_site_data(data_sources, container, token)


def import_site_data(data_sources, container, token):
    auto_import_data_sources = ['Vula_Memberships', 'Vula_Gradebook']

    data_source_check = do_all_data_sources_exist(data_sources, auto_import_data_sources)

    # If containers have no data sources -> create memberships and gradebook
    if not data_sources or not data_source_check:
        url = ONTASK['url'] + 'datasource/'
        create_data_sources(container, url, token, auto_import_data_sources)

    for data_source in data_sources:
        if data_source['name'] not in auto_import_data_sources:
            continue

        url = ONTASK['url'] + 'datasource/' + data_source['id'] + '/'
        update_data_sources(container, url, token, data_source)


update_container_data()
