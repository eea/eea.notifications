from Products.Five.browser import BrowserView
from plone import api
import os
# from land.copernicus.content.config import ENV_HOST_USERS_STATS

# ENV_HOST_USERS_STATS = ENVPATH('LAND_HOST_USERS_STATS', 'land.copernicus.eu')
# HOST = ENV_HOST_USERS_STATS

# [TODO] Config file + env


def ENVPATH(name, default=None):
    """ GET path from os env
    """
    path = os.environ.get(name)
    if not path and default is None:
        raise EnvironmentError('{} needs to be defined!'.format(name))
    else:
        return path or default


HOST = ENVPATH('NOTIFICATIONS_CENTER_HOST', 'climate-adapt.eea.europa.eu')
PLONE = "/cca"


def get_plone_site():
    import Zope2
    app = Zope2.app()
    from Testing.ZopeTestCase import utils
    utils._Z2HOST = HOST

    path = PLONE.split('/')

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
