""" The user's form for managing tags subscriptions
"""
from Products.Five.browser import BrowserView


class UserTagsForm(BrowserView):
    """ User tags form
        User subscribes to a list of tags (from all content tags available).
        """

    def get_tags(self):
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

    def set_tags(self, tags):
        """ Save user preferences
        """
        # [TODO] WIP
        print "Saved: {0}".format(tags)

    def __call__(self):
        if "submit" in self.request.form:
            tags = []
            value = self.request.form.get('tags-list', [])
            if isinstance(value, basestring):
                tags.append(value)
            else:
                tags = value
            self.set_tags(tags)
        return self.index()
