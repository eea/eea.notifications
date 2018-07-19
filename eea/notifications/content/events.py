""" Events
"""
from eea.notifications.catalogtool import get_catalog
from plone import api


def add_or_update_in_catalog(obj, event):
    """ Reindex object in EEA Notifications Catalog
    """
    site = api.portal.get()
    eea_notifications_catalog = get_catalog(site)
    eea_notifications_catalog.catalog_object(
        obj,
        idxs=(
            'getTags',
        ),
        update_metadata=1
    )


def remove_from_catalog(obj, event):
    """ Remove object from EEA Notifications Catalog
    """
    site = api.portal.get()
    eea_notifications_catalog = get_catalog(site)
    eea_notifications_catalog.uncatalog_object(obj.absolute_url_path())
