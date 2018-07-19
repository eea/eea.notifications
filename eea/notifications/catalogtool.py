""" The Notifications catalog
    Global persistent utility that holds the catalog
"""

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.CMFCore.permissions import ManagePortal
from Products.CMFPlone.CatalogTool import CatalogTool
from Products.ZCatalog.ZCatalog import ZCatalog
from eea.notifications.interfaces.catalog import IEEANotificationsCatalogTool
from eea.notifications.utils import LOGGER
from eea.notifications.utils import list_content_types
from plone import api
from zope.interface import implements
import transaction


def get_catalog(context):
    """ Return the Notifications catalog
    """
    return api.portal.get_tool(name="eea_notifications_catalog")


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

    def enumerateIndexes(self):
        """Returns indexes used by catalog"""
        return (
            ('getTags', 'KeywordIndex', ()),
            )

    security.declarePublic('enumerateMetadata')

    def enumerateMetadata(self):
        """Returns metadata used by catalog"""
        return (
            'getTags',
           )

    security.declareProtected(ManagePortal, 'clearFindAndRebuild')

    def clearFindAndRebuild(self):
        """Empties catalog, then finds all contentish objects (i.e. objects
           with an indexObject method), and reindexes them.
           This may take a long time.
        """

        def indexObject(obj, path):
            self.reindexObject(obj)

        self.manage_catalogClear()

        portal = api.portal.get()
        portal.ZopeFindAndApply(
            portal,
            # """ put your meta_type here """,

            obj_metatypes=(),

            search_sub=True, apply_func=indexObject)

    def catalog_rebuild(context):
        portal_catalog = api.portal.get_tool('portal_catalog')
        eea_notifications_catalog = get_catalog(context)

        for portal_type in list_content_types():
            brains = portal_catalog(portal_type=portal_type)
            brains_len = len(brains)
            LOGGER.info('Found %s brains.', brains_len)
            objects = (brain.getObject() for brain in brains)
            for idx, item in enumerate(objects, start=1):
                eea_notifications_catalog.catalog_object(
                    item,
                    idxs=(
                        'getTags',
                    ),
                    update_metadata=1
                )
                if idx % 50 == 0:
                    LOGGER.info('Done %s/%s.', idx, brains_len)
            transaction.savepoint()

    def all_tags(self):
        """ The list of available content tags
        """
        tags = self.uniqueValuesFor("getTags")

        return [(x, x) for x in sorted(tags)]

    def selected_tags(self, user_id):
        """ The list of user selected tags
        """
        user = api.user.get(user_id)
        return user.getProperty("eea_notifications_tags")

    def set_tags(self, tags, user_id):
        """ Save user preferences
        """
        user = api.user.get(user_id)
        user.setProperties(eea_notifications_tags=tags)

    def all_events(self):
        """ The list of available content events
        """
        # [TODO] WIP
        return [
            ('added', 'Added'),
            ('edited', 'Edited'),
            ('deleted', 'Deleted'),
        ]

    def selected_events(self, user_id):
        """ The list of user selected events
        """
        user = api.user.get(user_id)
        return user.getProperty("eea_notifications_events")

    def set_events(self, events, user_id):
        """ Save user preferences
        """
        user = api.user.get(user_id)
        user.setProperties(eea_notifications_events=events)


InitializeClass(EEANotificationsCatalogTool)
