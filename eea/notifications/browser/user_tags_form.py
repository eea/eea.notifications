""" The user's form for managing tags subscriptions
"""
from Products.Five.browser import BrowserView
from eea.notifications.catalogtool import get_catalog
from plone import api


class UserTagsForm(BrowserView):
    """ User tags form
        User subscribes to a list of tags (from all content tags available).
        """

    @property
    def notifications_catalog(self):
        return get_catalog(self.context)

    @property
    def user_id(self):
        """ The current user's id
        """
        return api.user.get_current().getId()

    def __call__(self):
        import pdb; pdb.set_trace()
        if "submit" in self.request.form:
            tags = []
            value = self.request.form.get('tags-list', [])
            if isinstance(value, basestring):
                tags.append(value)
            else:
                tags = value
            self.notifications_catalog.set_tags(tags, self.user_id)
        return self.index()
