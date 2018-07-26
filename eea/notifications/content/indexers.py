from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import IMemberData
from eea.notifications.utils import get_tags
from plone.indexer.decorator import indexer


@indexer(IContentish)
def getTags(obj):
    """ To be improved if we want to include other fields
    """
    return get_tags(obj)


@indexer(IMemberData)
def getUserTags(obj):
    """ The tags an user subscribed to
    """
    return obj.getProperty("eea_notifications_tags")
