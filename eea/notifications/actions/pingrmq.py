""" The Ping RabbitMQ
"""

from OFS.SimpleItem import SimpleItem
from eea.notifications.config import RABBIT_QUEUE
from eea.notifications.interfaces import IPingRMQAction
from eea.notifications.utils import LOGGER
from eea.notifications.utils import get_rabbit_config
from eea.notifications.utils import get_tags
from eea.rabbitmq.client import RabbitMQConnector
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.app.layout.viewlets.content import ContentHistoryView
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from zope.component import adapts
from zope.formlib import form
from zope.interface import Interface
from zope.interface import implements
import json


class PingRMQAction(SimpleItem):
    """ Ping action settings
    """
    implements(IPingRMQAction, IRuleElementData)

    related_action = ''
    notification_subject = ''
    notification_action = ''
    element = 'eea.notifications.actions.PingRMQ'
    summary = u'Ping RabbitMQ'


class PingRMQActionExecutor(object):
    """ Ping action executor
    """
    implements(IExecutable)
    adapts(Interface, IPingRMQAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        related_action = self.element.related_action
        notification_subject = self.element.notification_subject
        notification_action = self.element.notification_action

        obj = self.event.object
        path = "/".join(obj.getPhysicalPath())

        tags = get_tags(obj)

        try:
            url = obj.absolute_url()
        except Exception:
            url = "N/A"

        try:
            content_title = obj.Title()
        except Exception:
            content_title = "N/A"

        try:
            actor = ContentHistoryView(
                    obj, self.context.REQUEST).fullHistory()[0][
                            'actor']['username']
        except Exception:
            try:
                actor = obj.Creator()
            except Exception:
                actor = "N/A"

        rabbit_config = get_rabbit_config()
        rabbit = RabbitMQConnector(**rabbit_config)
        try:
            rabbit.open_connection()
            rabbit.declare_queue(RABBIT_QUEUE)

            json_notification = {
                'notification_subject': notification_subject,
                'notification_action': notification_action,
                'content_url': url,
                'content_title': content_title,
                'actor': actor,
                'path': path,
                'tags': tags,
                'events': related_action,
            }
            message = json.dumps(json_notification)

            rabbit.send_message(RABBIT_QUEUE, message)
        except Exception:
            LOGGER.error(
                "RabbitMQ connection problem. "
                "Check client configuration: /@@rabbitmq-client-controlpanel."
                " See example in documentation.")


class PingRMQAddForm(AddForm):
    """ Ping action addform
    """
    form_fields = form.FormFields(IPingRMQAction)
    label = u"Add Ping RabbitMQ Action"
    description = u"A ping RabbitMQ action."
    form_name = u"Configure element"

    def create(self, data):
        """ Ping action create method
        """
        a = PingRMQAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class PingRMQEditForm(EditForm):
    """ Ping action editform
    """
    form_fields = form.FormFields(IPingRMQAction)
    label = u"Edit Ping RabbitMQ Action"
    description = u"A ping RabbitMQ action."
    form_name = u"Configure element"
