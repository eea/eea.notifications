""" Events
"""
from eea.notifications.catalogtool import get_catalog
from plone import api


def update_catalog(obj, event):
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
