""" The Ping RabbitMQ
"""

from OFS.SimpleItem import SimpleItem
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from zope import schema
from zope.component import adapts
from zope.formlib import form
from zope.interface import Interface
from zope.interface import implements


class IPingRMQAction(Interface):
    """ Ping action settings schema
    """
    test_setting = schema.TextLine(
        title=u"Setting",
        description=u"Setting description.",
        required=True
    )


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

        print(event, test_setting, obj, container)

        # create = IObjectAddedEvent.providedBy(event)


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
