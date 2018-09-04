from zope import schema
from zope.interface import Interface


class IPingRMQAction(Interface):
    """ Ping action settings schema
    """
    related_action = schema.Choice(
        title=u"Related action",
        description=u"What happened with your content item in this case.",
        vocabulary="events_vocab",
        required=True
    )

    notification_subject = schema.TextLine(
        title=u"Notification subject",
        description=u"""
        Available as ${eea_notifications_notification_subject}
        in mail action of a content rule responsible for sending notification.
        """,
        required=False
    )

    notification_action = schema.TextLine(
        title=u"Notification action",
        description=u"""
        Available as ${eea_notifications_notification_action}
        in mail action of a content rule responsible for sending notification.
        """,
        required=False
    )
