""" Notifications Center - the script and the browser view
"""

from Products.CMFCore.interfaces import IContentish
from Products.Five.browser import BrowserView
from eea.notifications.actions.events import SendEEANotificationEvent
from eea.notifications.config import ANNOT_SUBS_KEY
from eea.notifications.config import ENV_HOST_NAME
from eea.notifications.config import ENV_PLONE_NAME
from eea.notifications.config import RABBIT_QUEUE
# from eea.notifications.notifications import send_email_notification
from eea.notifications.utils import LOGGER
from eea.notifications.utils import get_object_having_path
from eea.notifications.utils import get_rabbit_config
from eea.rabbitmq.client import RabbitMQConnector
from plone import api
from plone.stringinterp.adapters import BaseSubstitution
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.event import notify
from zope.globalrequest import getRequest
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


def msg_part(req, key):
    """ return the value of given key for a notification
    """
    msg = json.loads(IAnnotations(req).get(ANNOT_SUBS_KEY))
    return msg.get(key, "")


class subs_user_id(BaseSubstitution):
    adapts(IContentish)

    category = u'EEA Notifications'
    description = u"The user_id of notified person."

    def safe_call(self):
        req = getRequest()
        return msg_part(req, "user_id")


class subs_user_email(BaseSubstitution):
    adapts(IContentish)

    category = u'EEA Notifications'
    description = u"The email of notified person."

    def safe_call(self):
        req = getRequest()
        user_id = msg_part(req, "user_id")

        membership_tool = api.portal.get_tool('portal_membership')
        user = membership_tool.getMemberById(user_id)
        email = user.getProperty('email')
        return email


class subs_notification_subject(BaseSubstitution):
    adapts(IContentish)

    category = u'EEA Notifications'
    description = u"The subject as defined in pingRMQ form."

    def safe_call(self):
        req = getRequest()
        return msg_part(req, "notification_subject")


class subs_notification_action(BaseSubstitution):
    adapts(IContentish)

    category = u'EEA Notifications'
    description = u"The action on that content (example: edited)."

    def safe_call(self):
        req = getRequest()
        return msg_part(req, "notification_action")


class subs_content_url(BaseSubstitution):
    adapts(IContentish)

    category = u'EEA Notifications'
    description = u"The url of content related to this event."

    def safe_call(self):
        req = getRequest()
        return msg_part(req, "content_url")


class subs_actor(BaseSubstitution):
    adapts(IContentish)

    category = u'EEA Notifications'
    description = u"The user_id of the event's actor."

    def safe_call(self):
        req = getRequest()
        return msg_part(req, "actor")


def notifications_center_operations(site):
    """ All the operations of Notifications Center happen here
        Callable by both: browser view and script
    """

    def operations(message, site):
        msg = json.loads(message)

        print message
        obj = get_object_having_path(msg['path'])
        if obj is not None:
            notify(SendEEANotificationEvent(obj, message))
        else:
            LOGGER.error("Object with path {0} not found.".msg['path'])

        # TODO Remove this:
        # send_email_notification(
        #     user_id=msg['user_id'],
        #     notification_subject=msg['notification_subject'],
        #     notification_action=msg['notification_action'],
        #     content_url=msg['content_url'],
        #     actor=msg['actor']
        # )
        return True

    # Consume messages from queue
    rabbit_config = get_rabbit_config()
    rabbit = RabbitMQConnector(**rabbit_config)
    try:
        LOGGER.info('START consuming from \'%s\'', RABBIT_QUEUE)
        rabbit.open_connection()
        rabbit.declare_queue(RABBIT_QUEUE)

        while True:
            method, properties, body = rabbit.get_message(RABBIT_QUEUE)
            if method is None and properties is None and body is None:
                LOGGER.info('Queue is empty \'%s\'.', RABBIT_QUEUE)
                break

            operations(body, site)
            rabbit.get_channel().basic_ack(delivery_tag=method.delivery_tag)

        rabbit.close_connection()
        LOGGER.info('DONE consuming from \'%s\'', RABBIT_QUEUE)
    except AttributeError:
        LOGGER.error("Wrong configuration for RabbitMQ client.")


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
