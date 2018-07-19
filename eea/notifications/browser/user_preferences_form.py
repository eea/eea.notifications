""" The user's form for managing tags and events subscriptions
"""
from Products.Five.browser import BrowserView
from eea.notifications.catalogtool import get_catalog
from plone import api


class UserPreferencesForm(BrowserView):
    """ User's preferences form
        User subscribes to a list of tags (from all content tags available).
        Also selects the events he wants to follow.
    """

    @property
    def notifications_catalog(self):
        return get_catalog()

    @property
    def user_id(self):
        """ The current user's id
        """
        return api.user.get_current().getId()

    def __call__(self):
        if "submit" in self.request.form:
            tags = []
            value = self.request.form.get('tags-list', [])
            if isinstance(value, basestring):
                tags.append(value)
            else:
                tags = value
            self.notifications_catalog.set_tags(tags, self.user_id)

            events = []
            value = self.request.form.get('events-list', [])
            if isinstance(value, basestring):
                events.append(value)
            else:
                events = value
            self.notifications_catalog.set_events(events, self.user_id)
        return self.index()
