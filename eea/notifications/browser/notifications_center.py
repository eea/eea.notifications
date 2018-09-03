""" Notifications Center - the script and the browser view
"""

from Products.Five.browser import BrowserView
from eea.notifications.actions.events import SendEEANotificationEvent
from eea.notifications.config import ENV_HOST_NAME
from eea.notifications.config import ENV_PLONE_NAME
from eea.notifications.config import RABBIT_QUEUE
from eea.notifications.utils import LOGGER
from eea.notifications.utils import get_object_having_path
from eea.notifications.utils import get_rabbit_config
from eea.rabbitmq.client import RabbitMQConnector
from plone import api
from plone.app.contentrules.handlers import close
from zope.event import notify
import json


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

    def operations(message, site):
        msg = json.loads(message)

        print message

        obj = get_object_having_path(msg['path'])
        if obj is not None:
            evt = SendEEANotificationEvent(obj, message)
            notify(evt)
            close(evt)  # make sure it will work for multiple notify(
        else:
            LOGGER.error("Object with path {0} not found.".format(msg['path']))

        return True

    # Consume messages from queue
    rabbit_config = get_rabbit_config()
    rabbit = RabbitMQConnector(**rabbit_config)

    ok_configuration = True
    try:
        LOGGER.info('START consuming from \'%s\'', RABBIT_QUEUE)
        rabbit.open_connection()
        rabbit.declare_queue(RABBIT_QUEUE)
    except AttributeError:
        LOGGER.error("Wrong configuration for RabbitMQ client.")
        ok_configuration = False

    if ok_configuration:
        while True:
            method, properties, body = rabbit.get_message(RABBIT_QUEUE)
            if method is None and properties is None and body is None:
                LOGGER.info('Queue is empty \'%s\'.', RABBIT_QUEUE)
                break

            operations(body, site)
            rabbit.get_channel().basic_ack(delivery_tag=method.delivery_tag)

        rabbit.close_connection()
        LOGGER.info('DONE consuming from \'%s\'', RABBIT_QUEUE)


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
