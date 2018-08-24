# -*- coding: utf-8 -*-
from eea.notifications.tests.utils import NOTIFICATIONS_INTEGRATION_TESTING
from eea.notifications.tests.utils import log
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
import unittest


class UserPreferencesFormIntegrationTest(unittest.TestCase):

    layer = NOTIFICATIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_user_preferences_form(self):
        # import pdb; pdb.set_trace()
        log("user_preferences_form", "WIP.")
        self.assertTrue(True)


class TestUserPreferencesForm(unittest.TestCase):

    def test_user_preferences_form(self):
        log("user_preferences_form", "WIP.")

        self.assertTrue(True)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
