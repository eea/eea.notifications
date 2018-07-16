from plone.indexer.decorator import indexer
from Products.CMFCore.interfaces import IContentish


@indexer(IContentish)
def getTags(obj):
    return "[TODO] WIP list of tags"
