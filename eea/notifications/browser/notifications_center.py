""" Notifications Center - the script and the browser view
"""

from Products.Five.browser import BrowserView
from eea.notifications.catalogtool import get_catalog
from eea.notifications.config import ENV_HOST_NAME
from eea.notifications.config import ENV_PLONE_NAME
from eea.notifications.config import RABBIT_QUEUE
from eea.notifications.notifications import send_email_notification
from eea.notifications.utils import LOGGER
from eea.notifications.utils import get_rabbit_config
from eea.rabbitmq.client import RabbitMQConnector
from plone import api
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
    # For testing:
    catalog = get_catalog()
    catalog.set_tags(tags=['Austria'], user_id='tibiadmin')
    catalog.set_events(events=['deleted'], user_id='tibiadmin')
    users = catalog.search_users_by_preferences(
        events=['deleted', 'edited'],
        tags=['Austria'],
        mode="or"
    )
    users = users

    def operations(message):
        msg = json.loads(message)

        print message
        send_email_notification(
            user_id=msg['user_id'],
            notification_subject=msg['notification_subject'],
            notification_action=msg['notification_action'],
            content_url=msg['content_url'],
            actor=msg['actor']
        )
        return True

    # Consume messages from queue
    rabbit_config = get_rabbit_config()
    rabbit = RabbitMQConnector(**rabbit_config)
    LOGGER.info('START consuming from \'%s\'', RABBIT_QUEUE)
    rabbit.open_connection()
    rabbit.declare_queue(RABBIT_QUEUE)

    while True:
        method, properties, body = rabbit.get_message(RABBIT_QUEUE)
        if method is None and properties is None and body is None:
            LOGGER.info('Queue is empty \'%s\'.', RABBIT_QUEUE)
            break

        operations(body)
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
