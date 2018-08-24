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
        try:
            form = api.portal.get().unrestrictedTraverse("user_preferences")
            log("browser/user_preferences_form", "Form exists.")
        except Exception:
            form = None
            log("browser/user_preferences_form", "Problems related to form.")
        self.assertTrue("SimpleViewClass" in str(form))
        self.assertTrue("/templates/user_preferences_form" in str(form))


class TestUserPreferencesForm(unittest.TestCase):

    def test_user_preferences_form(self):
        try:
            from eea.notifications.browser.user_preferences_form import \
                UserPreferencesForm
            log("browser/user_preferences_form", "Form is defined.")
        except Exception:
            UserPreferencesForm = None
            log("browser/user_preferences_form", "Form is missing.", "error")
        self.assertTrue(UserPreferencesForm is not None)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
