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

    notification_subject = schema.TextLine(
        title=u"Notification subject",
        description=u"The subject used in sent notification for this event",
        required=True
    )

    notification_action = schema.TextLine(
        title=u"Notification action",
        description=u"Description about what happened with your content used \
                in notification. The content was ...",
        required=True
    )
