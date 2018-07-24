""" Events
"""
from eea.notifications.catalogtool import get_catalog
from eea.notifications.utils import LOGGER


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


def object_modified(obj, event):
    """ Content was modified
    """
    add_or_update_in_catalog(obj, event)
    LOGGER.info("ZZZ Content was modified.")


def object_moved(obj, event):
    """ Content was moved
    """
    add_or_update_in_catalog(obj, event)
    LOGGER.info("ZZZ Content was moved.")


def object_added(obj, event):
    """ Content was added
    """
    add_or_update_in_catalog(obj, event)
    LOGGER.info("ZZZ Content was added.")


def object_removed(obj, event):
    """ Content was removed
    """
    remove_from_catalog(obj, event)
    LOGGER.info("ZZZ Content was removed.")
