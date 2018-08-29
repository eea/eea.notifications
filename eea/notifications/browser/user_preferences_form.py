""" The user's form for managing tags and events subscriptions
"""

from Products.Five.browser import BrowserView
from eea.notifications.catalogtool import get_catalog
from plone import api
from plone.directives import form
from z3c.form import button
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields
from zope.schema import Choice
from zope.schema import List


class IManageSubscriptionsForm(form.Schema):

    tags = List(
        title=u"Tags",
        value_type=Choice(vocabulary="tags_vocab"),
        required=False,
    )

    events = List(
        title=u"Events",
        value_type=Choice(vocabulary="events_vocab"),
        required=False,
    )


class ManageSubscriptionsForm(form.SchemaForm):
    """ The user preferences related to notifications form
    """

    schema = IManageSubscriptionsForm
    ignoreContext = True

    label = u"Manage subscriptions"
    description = u"""
        1. Select the content tags you are interested in.
        2. Select the type of events you want to be notified about."""

    fields = Fields(IManageSubscriptionsForm)
    fields['tags'].widgetFactory = CheckBoxFieldWidget
    fields['events'].widgetFactory = CheckBoxFieldWidget

    @property
    def notifications_catalog(self):
        return get_catalog()

    @property
    def user_id(self):
        """ The current user's id
        """
        return api.user.get_current().getId()

    @button.buttonAndHandler(u'Update subscriptions')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.notifications_catalog.set_tags(data['tags'], self.user_id)
        self.notifications_catalog.set_events(data['events'], self.user_id)
        self.status = "Your preferences have been updated."

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """ User cancelled. Redirect back to the front page.
        """


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
