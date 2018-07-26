""" The Ping RabbitMQ
"""

from OFS.SimpleItem import SimpleItem
from eea.notifications.catalogtool import get_catalog
from eea.notifications.interfaces import IPingRMQAction
from eea.notifications.utils import LOGGER
from eea.notifications.utils import get_tags
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
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

    test_setting = ''

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
        test_setting = self.element.test_setting
        obj = self.event.object
        container = obj.getParentNode()

        catalog = get_catalog()
        tags = get_tags(obj)
        events = [x[0] for x in catalog.all_events()]  # TODO use current event
        users = catalog.search_users_by_preferences(
            tags=tags, events=events, mode="or")

        # TODO Ping RabbitMQ with following info:
        info = [event, obj, container, tags, events, users, test_setting]
        info = info
        LOGGER.info(obj)


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
