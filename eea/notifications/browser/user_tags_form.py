""" The user's form for managing tags subscriptions
"""
from Products.Five.browser import BrowserView
from plone import api


class UserTagsForm(BrowserView):
    """ User tags form
        User subscribes to a list of tags (from all content tags available).
        """

    @property
    def all_tags(self):
        """ The list of available content tags
        """
        # [TODO] WIP
        return [
            ('education', 'Education'),
            ('security', 'Security'),
            ('agriculture', 'Agriculture'),
            ('books', 'Books'),
            ('lorem-ipsum', 'Lorem ipsum')
        ]

    @property
    def selected_tags(self):
        """ The list of user selected tags
        """
        # [TODO] WIP
        return ['education', 'books']

    def set_tags(self, tags, user_id):
        """ Save user preferences
        """
        # [TODO] WIP
        print "Saved: {0} for {1}".format(tags, user_id)

    def __call__(self):
        if "submit" in self.request.form:
            tags = []
            value = self.request.form.get('tags-list', [])
            if isinstance(value, basestring):
                tags.append(value)
            else:
                tags = value
            user_id = api.user.get_current().getId()
            self.set_tags(tags, user_id)
        return self.index()
