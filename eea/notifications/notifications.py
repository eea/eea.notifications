""" Mail notification related
"""
from Products.CMFCore.interfaces import IContentish
from eea.notifications.config import ANNOT_SUBS_KEY
from plone import api
from plone.stringinterp.adapters import BaseSubstitution
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.globalrequest import getRequest
import json


def msg_part(req, key):
    """ return the value of given key for a notification
    """
    msg = json.loads(IAnnotations(req).get(ANNOT_SUBS_KEY))
    return msg.get(key, "")


class subs_user_id(BaseSubstitution):
    adapts(IContentish)

    category = u'EEA Notifications'
    description = u"The user_id of notified person."

    def safe_call(self):
        req = getRequest()
        return msg_part(req, "user_id")


class subs_user_email(BaseSubstitution):
    adapts(IContentish)

    category = u'EEA Notifications'
    description = u"The email of notified person."

    def safe_call(self):
        req = getRequest()
        user_id = msg_part(req, "user_id")

        membership_tool = api.portal.get_tool('portal_membership')
        user = membership_tool.getMemberById(user_id)
        email = user.getProperty('email')
        return email


class subs_notification_subject(BaseSubstitution):
    adapts(IContentish)

    category = u'EEA Notifications'
    description = u"The subject as defined in pingRMQ form."

    def safe_call(self):
        req = getRequest()
        return msg_part(req, "notification_subject")


class subs_notification_action(BaseSubstitution):
    adapts(IContentish)

    category = u'EEA Notifications'
    description = u"The action on that content (example: edited)."

    def safe_call(self):
        req = getRequest()
        return msg_part(req, "notification_action")


class subs_content_url(BaseSubstitution):
    adapts(IContentish)

    category = u'EEA Notifications'
    description = u"The url of content related to this event."

    def safe_call(self):
        req = getRequest()
        return msg_part(req, "content_url")


class subs_actor(BaseSubstitution):
    adapts(IContentish)

    category = u'EEA Notifications'
    description = u"The user_id of the event's actor."

    def safe_call(self):
        req = getRequest()
        return msg_part(req, "actor")
