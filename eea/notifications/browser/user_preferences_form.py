""" The user's form for managing tags and events subscriptions
"""

from eea.notifications.catalogtool import get_catalog
from plone import api
from plone.directives import form
from z3c.form import button
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields
from zope.interface import provider
from zope.schema import Choice
from zope.schema import List
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def default_tags(context):
    return [x for x in get_catalog().selected_tags(
        user_id=api.user.get_current().id)]


@provider(IContextAwareDefaultFactory)
def default_events(context):
    return [x for x in get_catalog().selected_events(
        user_id=api.user.get_current().id)]


class IManageSubscriptionsForm(form.Schema):

    tags = List(
        title=u"1. Select the content tags you are interested in.",
        description=u"""
            Example: if you want to be notified when an item related to
            education is changed you will subscribe to "education" tag.
        """,
        value_type=Choice(vocabulary="tags_vocab"),
        defaultFactory=default_tags,
        required=False,
    )

    events = List(
        title=u"2. Select the type of events you want to be notified about.",
        description=u"""
            Example: the item was deleted. You will receive a notification
            when an item (tagged with a tag you are interested in) is deleted.
        """,
        value_type=Choice(vocabulary="events_vocab"),
        defaultFactory=default_events,
        required=False,
    )


class ManageSubscriptionsForm(form.SchemaForm):
    """ The user preferences related to notifications form
    """

    schema = IManageSubscriptionsForm
    ignoreContext = True

    label = u"Manage subscriptions"
    description = u"""
    Notify me on content (changes) that is tagged with selected tags.
    """

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
