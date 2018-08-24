# -*- coding: utf-8 -*-
from eea.notifications.tests.utils import NOTIFICATIONS_INTEGRATION_TESTING
from eea.notifications.tests.utils import log
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
import unittest


class CatalogToolIntegrationTest(unittest.TestCase):

    layer = NOTIFICATIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_catalogtool(self):
        from eea.notifications.catalogtool import get_catalog
        try:
            catalog = get_catalog()
            catalog = catalog  # happy PEP
            exists = True
        except Exception:
            exists = False

        if exists:
            log("catalogtool", "Custom catalog exists.")
            self.assertTrue(exists)
        else:
            log("catalogtool", "Custom catalog is missing.", "error")
            self.assertTrue(exists)

    def test_catalogtool_events_in_user_preferences(self):
        from eea.notifications.catalogtool import get_catalog

        # Try with a single event
        event = "something happened with this content"
        event_no = "something else happened"

        catalog = get_catalog()
        catalog.set_events(user_id=TEST_USER_ID, events=[event])
        selected = catalog.selected_events(user_id=TEST_USER_ID)
        if (event in selected) and (event_no not in selected):
            log("catalogtool",
                "Set events and get user selected ones is working.")
        else:
            log("catalogtool",
                "Set events and get user selected ones is not working.",
                "error")

        self.assertTrue(event in selected)
        self.assertTrue(event_no not in selected)

        # Try with multiple events
        events = ['edited_custom', 'deleted_custom']
        events_no = ['other_edited_custom', 'other_deleted_custom']

        catalog.set_events(user_id=TEST_USER_ID, events=events)
        selected = catalog.selected_events(user_id=TEST_USER_ID)
        ok = True
        for event in events:
            if event not in selected:
                ok = False

            self.assertTrue(event in selected)

        if ok:
            log("catalogtool",
                "Set multiple events and get user selected ones is working.")
        else:
            log("catalogtool",
                "Set multiple events and get user selected ones not working.",
                "error")

        ok = True
        for event_no in events_no:
            if event_no in selected:
                ok = False

            self.assertTrue(event_no not in selected)

        if ok:
            log("catalogtool", "Only set events are present.")
        else:
            log("catalogtool", "Wrong behaviour setting events.", "error")

    def test_catalogtool_tags_in_user_preferences(self):
        from eea.notifications.catalogtool import get_catalog

        # Try with a single tag
        tag = "a subject I like"
        tag_no = "not important"

        catalog = get_catalog()
        catalog.set_tags(user_id=TEST_USER_ID, tags=[tag])
        selected = catalog.selected_tags(user_id=TEST_USER_ID)
        if (tag in selected) and (tag_no not in selected):
            log("catalogtool",
                "Set tags and get user selected ones is working.")
        else:
            log("catalogtool",
                "Set tags and get user selected ones is not working.",
                "error")

        self.assertTrue(tag in selected)
        self.assertTrue(tag_no not in selected)

        # Try with multiple tags
        tags = ['subject 1', 'subject 2']
        tags_no = ['other 1', 'other 2']

        catalog.set_tags(user_id=TEST_USER_ID, tags=tags)
        selected = catalog.selected_tags(user_id=TEST_USER_ID)
        ok = True
        for tag in tags:
            if tag not in selected:
                ok = False

            self.assertTrue(tag in selected)

        if ok:
            log("catalogtool",
                "Set multiple tags and get user selected ones is working.")
        else:
            log("catalogtool",
                "Set multiple tags and get user selected ones not working.",
                "error")

        ok = True
        for tag_no in tags_no:
            if tag_no in selected:
                ok = False

            self.assertTrue(tag_no not in selected)

        if ok:
            log("catalogtool", "Only set tags are present.")
        else:
            log("catalogtool", "Wrong behaviour setting tags.", "error")

    def test_catalogtool_search_users_by_preferences(self):
        from eea.notifications.catalogtool import get_catalog

        events = ['modified_custom', 'deleted_custom']
        events_no = ['event 1', 'event 2']

        catalog = get_catalog()
        catalog.set_events(user_id=TEST_USER_ID, events=events)

        tags = ['subject 1', 'subject 2']
        tags_no = ['other 1', 'other 2']

        catalog.set_tags(user_id=TEST_USER_ID, tags=tags)

        users = catalog.search_users_by_preferences(
                events=events, tags=tags, mode="or")

        self.assertTrue(TEST_USER_ID in users)
        if TEST_USER_ID in users:
            log("catalogtool", "User found by preferences as expected.")
        else:
            log("catalogtool", "User not found by preferences.", "error")

        users = catalog.search_users_by_preferences(
                events=events_no, tags=tags_no, mode="or")

        self.assertTrue(TEST_USER_ID not in users)
        if TEST_USER_ID not in users:
            log("catalogtool", "Search results seems ok.")
        else:
            log("catalogtool", "Wrong search results.", "error")


class TestCatalogTool(unittest.TestCase):

    def test_catalogtool(self):
        log("catalogtool", "get_catalog function is defined.")

        from eea.notifications.catalogtool import get_catalog
        self.assertTrue('function' in str(type(get_catalog)))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
