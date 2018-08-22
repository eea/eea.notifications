""" Mail notification
"""

from eea.notifications.utils import LOGGER
from plone import api
from smtplib import SMTPRecipientsRefused


def send_email_notification(user_id, notification_subject='Notification',
                            notification_action='updated', content_url='',
                            actor='admin'):
    """ Notify user
    """
    site = api.portal.get()
    membership_tool = api.portal.get_tool('portal_membership')
    user = membership_tool.getMemberById(user_id)
    email = user.getProperty('email')
    email_from_name = site.getProperty('email_from_name', '')
    email_from_address = site.getProperty('email_from_address', '')
    mfrom = "{0} <{1}>".format(email_from_name, email_from_address)
    subject = notification_subject
    mail_text = u"""
Hello {0},
The content {1} was {2} by {3}.

Kind regards,
Someone""".format(user_id, content_url, notification_action, actor)

    LOGGER.info("ZZZZZ {0}, {1}, {2}, {3}".format(
        email, mfrom, subject, mail_text))
    try:
        mail_host = api.portal.get_tool(name='MailHost')
        return mail_host.simple_send(
            mto=email, mfrom=mfrom, subject=subject,
            body=mail_text, immediate=True)
    except SMTPRecipientsRefused:
        # raise SMTPRecipientsRefused('Recipient rejected by server')
        pass
