""" The Ping RabbitMQ
"""

from OFS.SimpleItem import SimpleItem
from eea.notifications.catalogtool import get_catalog
from eea.notifications.config import OBJECT_EVENTS
from eea.notifications.config import RABBIT_CONFIG
from eea.notifications.config import RABBIT_QUEUE
from eea.notifications.interfaces import IPingRMQAction
from eea.notifications.notifications import send_email_notification
from eea.notifications.utils import LOGGER
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


class PingRMQAction(SimpleItem):
    """ Ping action settings
    """
    implements(IPingRMQAction, IRuleElementData)

    related_actions = ''
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
        event = self.event
        related_actions = self.element.related_actions
        notification_subject = self.element.notification_subject
        notification_action = self.element.notification_action

        obj = self.event.object
        container = obj.getParentNode()

        catalog = get_catalog()
        tags = get_tags(obj)

        def get_actions_by_interface_names(event):
            """ Return human readable actions done on this event
            """
            return [action for action in OBJECT_EVENTS if action in ' '.join(
                [interface.__name__.lower() for interface in list(
                    set(event.__provides__.__iro__))]
                )]

        def get_actions():
            """ return related user preferred events types
            """
            return [action for action in OBJECT_EVENTS if action in
                    related_actions]

        actions = get_actions()
        if len(actions) == 0:
            actions = get_actions_by_interface_names(event)

        users = catalog.search_users_by_preferences(
            tags=tags, events=actions, mode="or")

        # TODO Ping RabbitMQ with following info:

        info = [event, obj, container, tags, actions, notification_subject,
                notification_action, users, related_actions]
        info = info
        LOGGER.info(obj)

        rabbit = RabbitMQConnector(**RABBIT_CONFIG)
        rabbit.open_connection()
        rabbit.declare_queue(RABBIT_QUEUE)
        rabbit.send_message(RABBIT_QUEUE, "ZZZ body text")
        rabbit.close_connection()

        # TODO Then notification center will send notifications:
        try:
            url = obj.absolute_url()
        except Exception:
            url = "ZZZ URL"
        try:
            actor = ContentHistoryView(
                    obj, self.context.REQUEST).fullHistory()[0][
                            'actor']['username']
        except Exception:
            actor = ""

        for user_id in users:
            send_email_notification(
                user_id=user_id,
                notification_subject=notification_subject,
                notification_action=notification_action,
                content_url=url,
                actor=actor
            )


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
