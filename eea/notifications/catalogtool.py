""" The Notifications catalog
    Global persistent utility that holds the catalog
"""

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
# from Products.CMFCore.permissions import ManagePortal
# from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.CatalogTool import CatalogTool
from Products.ZCatalog.ZCatalog import ZCatalog
from eea.notifications.interfaces.catalog import IEEANotificationsCatalogTool
from zope.interface import implements


class EEANotificationsCatalogTool(CatalogTool):
    """ The Notifications Catalog Tool
    """

    implements(IEEANotificationsCatalogTool)

    title = "EEA Notifications Catalog"
    id = 'eea_notifications_catalog'
    portal_type = meta_type = 'EEA Notifications Catalog Tool'
    plone_tool = 1

    security = ClassSecurityInfo()
    _properties = (
        {
            'id': 'title',
            'type': 'string',
            'mode': 'w'
        },)

    def __init__(self):
        ZCatalog.__init__(self, self.getId())

    security.declarePublic('enumerateIndexes')

    # def enumerateIndexes(self):
    #     """Returns indexes used by catalog"""
    #     return (
    #         ('id', 'FieldIndex', ()),
    #         ('portal_type', 'FieldIndex', ()),
    #         ('path', 'ExtendedPathIndex', ('getPhysicalPath')),
    #         ('getCanonicalPath', 'ExtendedPathIndex', ('getCanonicalPath')),
    #         ('isArchived', 'FieldIndex', ()),
    #         ('is_trashed', 'FieldIndex', ()),
    #         ('is_obsolete', 'FieldIndex', ()),
    #         ('Language', 'FieldIndex', ()),
    #         ('review_state', 'FieldIndex', ()),
    #         ('allowedRolesAndUsers', 'DPLARAUIndex', ()),
    #
    #         )
    #
    # security.declarePublic('enumerateMetadata')
    #
    # def enumerateMetadata(self):
    #     """Returns metadata used by catalog"""
    #     return (
    #         'Title',
    #         'getId',
    #         'UID',
    #         'review_state',
    #         'created',
    #         'modified',
    #        )
    #
    # security.declareProtected(ManagePortal, 'clearFindAndRebuild')
    #
    # def clearFindAndRebuild(self):
    #     """Empties catalog, then finds all contentish objects (i.e. objects
    #        with an indexObject method), and reindexes them.
    #        This may take a long time.
    #     """
    #
    #     def indexObject(obj, path):
    #         self.reindexObject(obj)
    #
    #     self.manage_catalogClear()
    #
    #     portal = getToolByName(self, 'portal_url').getPortalObject()
    #     portal.ZopeFindAndApply(
    #         portal,
    #         # """ put your meta_type here """,
    #
    #         obj_metatypes=(),
    #
    #         search_sub=True, apply_func=indexObject)


InitializeClass(EEANotificationsCatalogTool)
