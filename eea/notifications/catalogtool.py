""" The Notifications catalog
    Global persistent utility that holds the catalog
"""

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.CMFCore.permissions import ManagePortal
from Products.CMFPlone.CatalogTool import CatalogTool
from Products.ZCatalog.ZCatalog import ZCatalog
from eea.notifications.config import ANNOT_EVENTS_KEY
from eea.notifications.config import ANNOT_TAGS_KEY
from eea.notifications.interfaces.catalog import IEEANotificationsCatalogTool
from eea.notifications.utils import LOGGER
from eea.notifications.utils import list_content_types
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from plone import api
from zope.annotation import IAnnotations
from zope.interface import implements
import transaction


def get_catalog():
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
            ('getUserTags', 'KeywordIndex', ()),
            )

    security.declarePublic('enumerateMetadata')

    def enumerateMetadata(self):
        """Returns metadata used by catalog"""
        return (
            'getTags',
            'getUserTags'
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

    def update_users_preferences(self, user_id=None):
        """ Synchronize annotations with memberdata field for all users
            or for given user
        """
        tags_annot = IAnnotations(api.portal.get()).setdefault(
            ANNOT_TAGS_KEY, PersistentDict({}))

        events_annot = IAnnotations(api.portal.get()).setdefault(
            ANNOT_EVENTS_KEY, PersistentDict({}))

        md = api.portal.get_tool("portal_memberdata")
        _members = md._members

        if user_id is None:
            for idx, user_id in enumerate(_members.iterkeys()):
                print "{0}: {1}".format(idx, user_id)
                user_member_data = _members.get(user_id)

                if user_member_data is not None:
                    # TODO Not sure the real values are saved
                    try:
                        tags = user_member_data.eea_notifications_tags
                    except AttributeError:
                        tags = []

                    tags_annot[user_id] = PersistentList(tags)

                    try:
                        events = user_member_data.eea_notifications_events
                    except AttributeError:
                        events = []

                    events_annot[user_id] = PersistentList(events)
        else:
            user_member_data = api.user.get(user_id)
            if user_member_data is not None:
                tags = user_member_data.getProperty('eea_notifications_tags')
                tags_annot[user_id] = PersistentList(tags)

                events = user_member_data.getProperty(
                    'eea_notifications_events')

                events_annot[user_id] = PersistentList(events)
        transaction.commit()

    def catalog_rebuild(context):
        portal_catalog = api.portal.get_tool('portal_catalog')
        eea_notifications_catalog = get_catalog()

        for portal_type in list_content_types():
            brains = portal_catalog(portal_type=portal_type)
            brains_len = len(brains)
            LOGGER.info('Found %s brains.', brains_len)
            objects = (brain.getObject() for brain in brains)
            for idx, item in enumerate(objects, start=1):
                eea_notifications_catalog.catalog_object(
                    item,
                    idxs=('getTags',),
                    update_metadata=1
                )
                if idx % 50 == 0:
                    LOGGER.info('Done %s/%s.', idx, brains_len)
            transaction.savepoint()

        eea_notifications_catalog.update_users_preferences()

    def all_tags(self):
        """ The list of available content tags
        """
        tags = self.uniqueValuesFor("getTags")

        return [(x, x) for x in sorted(tags)]

    def selected_tags(self, user_id):
        """ The list of user selected tags
        """
        tags_annot = IAnnotations(api.portal.get()).get(ANNOT_TAGS_KEY, None)
        if tags_annot is None:
            return []

        return tags_annot.get(user_id, [])
        # The same with:
        # user = api.user.get(user_id)
        # return user.getProperty("eea_notifications_tags")

    def set_tags(self, tags, user_id):
        """ Save user preferences
        """
        user = api.user.get(user_id)
        user.setMemberProperties({'eea_notifications_tags': tags})

        self.update_users_preferences(user_id=user_id)

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
        events_annot = IAnnotations(api.portal.get()).get(
            ANNOT_EVENTS_KEY, None)
        if events_annot is None:
            return []

        return events_annot.get(user_id, [])
        # The same with:
        # user = api.user.get(user_id)
        # return user.getProperty("eea_notifications_events")

    def set_events(self, events, user_id):
        """ Save user preferences
        """
        user = api.user.get(user_id)
        user.setMemberProperties({'eea_notifications_events': events})

        self.update_users_preferences(user_id=user_id)

    def search_users_by_preferences(self, events=[], tags=[], mode="or"):
        """ Return subscribers (list of usernames) for given events and tags

            mode: or - on of the criteria matches
                  and - only users subscribed to all given events and tags
        """
        tags_annot = IAnnotations(api.portal.get()).setdefault(
            ANNOT_TAGS_KEY, PersistentDict({}))

        events_annot = IAnnotations(api.portal.get()).setdefault(
            ANNOT_EVENTS_KEY, PersistentDict({}))

        mode = mode.lower()
        if mode == "and":
            has_tags = [
                x[0] for x in tags_annot.items() if set(
                    tags).issubset(x[1])]

            has_events = [
                x[0] for x in events_annot.items() if set(
                    events).issubset(x[1])]
            return set(has_tags).intersection(set(has_events))
        elif mode == "or":
            has_tags = [
                x[0] for x in tags_annot.items() if len(
                    set(tags).intersection(set(x[1]))) > 0]
            has_events = [
                x[0] for x in events_annot.items() if len(
                    set(events).intersection(set(x[1]))) > 0]

            return set(has_tags).intersection(set(has_events))


InitializeClass(EEANotificationsCatalogTool)
