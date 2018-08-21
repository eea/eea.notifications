""" The Ping RabbitMQ
"""

from OFS.SimpleItem import SimpleItem
from eea.notifications.catalogtool import get_catalog
from eea.notifications.config import OBJECT_EVENTS
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

        # TODO Ping RabbitMQ with following info:

        info = [event, obj, container, tags, actions, notification_subject,
                notification_action, users, related_actions, url, actor]
        info = info
        LOGGER.info(obj)

        rabbit_config = get_rabbit_config()
        rabbit = RabbitMQConnector(**rabbit_config)
        rabbit.open_connection()
        rabbit.declare_queue(RABBIT_QUEUE)

        def random_msg():
            import string
            import random
            return ''.join(
                random.choice(
                    string.ascii_uppercase + string.digits) for _ in range(8)
                )

        rabbit.send_message(RABBIT_QUEUE, random_msg())
        rabbit.send_message(RABBIT_QUEUE, random_msg())
        rabbit.send_message(RABBIT_QUEUE, random_msg())
        rabbit.close_connection()


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
