""" Events
"""
from eea.notifications.catalogtool import get_catalog
from eea.notifications.config import ANNOT_SUBS_KEY
from eea.notifications.interfaces import ISendEEANotificationEvent
from plone.app.contentrules.handlers import execute
from zope.annotation.interfaces import IAnnotations
from zope.component.interfaces import ObjectEvent
from zope.globalrequest import getRequest
from zope.interface import implements


class SendEEANotificationEvent(ObjectEvent):
    implements(ISendEEANotificationEvent)

    def __init__(self, context, message):
        self.object = context

        req = getRequest()
        IAnnotations(req)[ANNOT_SUBS_KEY] = message


def trigger_contentrules(event):
    execute(event.object, event)


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
