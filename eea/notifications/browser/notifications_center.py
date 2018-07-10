from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api


def notifications_center(site):
    """ The async script responsible for processing the pings and notify users
    """
    print "ZZZ Notified 1"
    print "ZZZ Notified 2"
    print "ZZZ Notified 3"


class NotificationsCenter(BrowserView):
    """ Notifications Center as view
    """
    index = ViewPageTemplateFile("templates/notifications_center.pt")

    def render(self):
        return self.index()

    @property
    def test_value(self):
        return "Test value"

    def __call__(self):
        site = api.portal.get()

        notifications_center(site)

        return self.render()
