from plone.indexer.decorator import indexer
from Products.CMFCore.interfaces import IContentish


@indexer(IContentish)
def getTags(obj):
    """ To be improved if we want to include other fields
    """
    try:
        tags = obj.subject
    except Exception:
        tags = ()
    return tags
