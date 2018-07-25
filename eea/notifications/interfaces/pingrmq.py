from zope import schema
from zope.component.interfaces import IObjectEvent
from zope.interface import Interface


class IPingRMQEvent(IObjectEvent):
    """ Ping event
    """


class IPingRMQAction(Interface):
    """ Ping action settings schema
    """
    test_setting = schema.TextLine(
        title=u"Setting",
        description=u"Setting description.",
        required=True
    )
