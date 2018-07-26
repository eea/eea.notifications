from zope import schema
from zope.interface import Interface


class IPingRMQAction(Interface):
    """ Ping action settings schema
    """
    test_setting = schema.TextLine(
        title=u"Setting",
        description=u"Setting description.",
        required=True
    )
