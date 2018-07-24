""" Notifications Center - the script and the browser view
"""

from Products.Five.browser import BrowserView
from eea.notifications.config import ENV_HOST_NAME
from eea.notifications.config import ENV_PLONE_NAME
from plone import api


def get_plone_site():
    import Zope2
    app = Zope2.app()
    from Testing.ZopeTestCase import utils
    utils._Z2HOST = ENV_HOST_NAME

    path = ENV_PLONE_NAME.split('/')

    app = utils.makerequest(app)
    app.REQUEST['PARENTS'] = [app]
    app.REQUEST.other['VirtualRootPhysicalPath'] = path
    from zope.globalrequest import setRequest
    setRequest(app.REQUEST)

    from AccessControl.SpecialUsers import system as user
    from AccessControl.SecurityManagement import newSecurityManager
    newSecurityManager(None, user)

    _site = app[path[-1]]
    site = _site.__of__(app)

    from zope.site.hooks import setSite
    setSite(site)

    return site


def notifications_center_operations(site):
    """ All the operations of Notifications Center happen here
        Callable by both: browser view and script
    """
    from eea.notifications.catalogtool import get_catalog
    import pdb; pdb.set_trace()
    catalog = get_catalog()
    catalog.set_tags(tags=['Austria'], user_id='tibiadmin')
    catalog.set_events(events=['deleted'], user_id='tibiadmin')
    users = catalog.search_users_by_preferences(
        events=['edited', 'deleted'],
        tags=['Austria', 'DRM'],
        mode="or"
    )
    print users
    print "ZZZ Notified 1"
    print "ZZZ Notified 2"
    print "ZZZ Notified 3"


def notifications_center():
    """ The script
        bin/zeo_client run bin/notifications_center
    """
    site = get_plone_site()
    notifications_center_operations(site)


class NotificationsCenter(BrowserView):
    """ Notifications Center as view
    """
    def __call__(self):
        site = api.portal.get()

        notifications_center_operations(site)

        return self.index()
