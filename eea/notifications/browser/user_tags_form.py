""" The user's form for managing tags subscriptions
"""
from Products.Five.browser import BrowserView


class UserTagsForm(BrowserView):
    """ User tags form
        User subscribes to a list of tags (from all content tags available).
        """

    def __call__(self):
        print "ZZZ"
        return self.index()
