from zope import schema
from zope.interface import Interface


class IPingRMQAction(Interface):
    """ Ping action settings schema
    """
    related_actions = schema.TextLine(
        title=u"Related actions",
        description=u"Use some words to describe the actions of this event. \
            (Example: modified edited changed) This field or event's \
            interface names is used to find subscribed users for this \
            type of event.",
        required=False
    )
