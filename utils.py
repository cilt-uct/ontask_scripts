from calls.ontask_login_calls import *


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



