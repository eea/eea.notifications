""" Events
"""
from eea.notifications.catalogtool import get_catalog
from eea.notifications.interfaces.events import IAnyContentChangesEvent
from eea.notifications.utils import LOGGER
from zope import event
from zope.interface import implementer


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
    event.notify(AnyContentChangesEvent(obj, evt))


def object_moved(obj, evt):
    """ Content was moved
    """
    add_or_update_in_catalog(obj, evt)
    event.notify(AnyContentChangesEvent(obj, evt))


def object_added(obj, evt):
    """ Content was added
    """
    add_or_update_in_catalog(obj, evt)
    event.notify(AnyContentChangesEvent(obj, evt))


def object_removed(obj, evt):
    """ Content was removed
    """
    remove_from_catalog(obj, evt)
    event.notify(AnyContentChangesEvent(obj, evt))


@implementer(IAnyContentChangesEvent)
class AnyContentChangesEvent(object):
    """ Event triggered when a content object is added,
        moved, edited or deleted.

        You can use it if you prefer a single content rule for all cases
        or you can use the default events in other case.
    """
    def __init__(self, context, evt, **kwargs):
        self.object = context
        self.event = evt
        LOGGER.info("ZZZZZZZ AnyContentChangesEvent")
