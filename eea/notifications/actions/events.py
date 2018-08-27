""" Events
"""
from eea.notifications.catalogtool import get_catalog
from eea.notifications.interfaces import ISendEEANotificationEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implements


class SendEEANotificationEvent(ObjectEvent):
    implements(ISendEEANotificationEvent)


def add_or_update_in_catalog(obj, evt):
    """ Reindex object in EEA Notifications Catalog
    """
    get_catalog().catalog_object(
        obj,
        idxs=(
            'getTags',
        ),
        update_metadata=1
    )


def remove_from_catalog(obj, evt):
    """ Remove object from EEA Notifications Catalog
    """
    get_catalog().uncatalog_object(obj.absolute_url_path())


def object_modified(obj, evt):
    """ Content was modified
    """
    add_or_update_in_catalog(obj, evt)


def object_moved(obj, evt):
    """ Content was moved
    """
    add_or_update_in_catalog(obj, evt)


def object_added(obj, evt):
    """ Content was added
    """
    add_or_update_in_catalog(obj, evt)


def object_removed(obj, evt):
    """ Content was removed
    """
    remove_from_catalog(obj, evt)
