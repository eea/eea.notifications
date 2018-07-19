""" Events
"""
from eea.notifications.catalogtool import get_catalog


def add_or_update_in_catalog(obj, event):
    """ Reindex object in EEA Notifications Catalog
    """
    get_catalog().catalog_object(
        obj,
        idxs=(
            'getTags',
        ),
        update_metadata=1
    )


def remove_from_catalog(obj, event):
    """ Remove object from EEA Notifications Catalog
    """
    get_catalog().uncatalog_object(obj.absolute_url_path())
