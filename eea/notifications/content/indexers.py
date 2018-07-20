from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import IMemberData
from plone.indexer.decorator import indexer


@indexer(IContentish)
def getTags(obj):
    """ To be improved if we want to include other fields
    """
    try:
        tags = obj.subject
    except Exception:
        tags = ()
    return tags


@indexer(IMemberData)
def getUserTags(obj):
    """ The tags an user subscribed to
    """
    return obj.getProperty("eea_notifications_tags")
