# -*- coding: utf-8 -*-
from eea.notifications.tests.utils import NOTIFICATIONS_INTEGRATION_TESTING
from eea.notifications.tests.utils import log
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
import unittest


class NotificationsCenterIntegrationTest(unittest.TestCase):

    layer = NOTIFICATIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_notifications_center(self):
        try:
            view = api.portal.get().unrestrictedTraverse(
                    "notifications_center")
            log("browser/notifications_center", "View exists.")
        except Exception:
            view = None
            log("browser/notifications_center", "Problems related to view.")
        self.assertTrue("SimpleViewClass" in str(view))
        self.assertTrue("/templates/notifications_center" in str(view))


class TestNotificationsCenter(unittest.TestCase):

    def test_notifications_center(self):
        try:
            from eea.notifications.browser.notifications_center import \
                get_plone_site
            log("browser/notifications_center", "get_plone_site is defined.")
        except Exception:
            get_plone_site = None
            log("browser/notifications_center",
                "get_plone_site is missing.", "error")
        self.assertTrue(get_plone_site is not None)

        try:
            from eea.notifications.browser.notifications_center import \
                notifications_center_operations as nco
            log("browser/notifications_center",
                "notifications_center_operations is defined.")
        except Exception:
            nco = None
            log("browser/notifications_center",
                "notifications_center_operations is missing.", "error")
        self.assertTrue(nco is not None)

        try:
            from eea.notifications.browser.notifications_center import \
                notifications_center as nc
            log("browser/notifications_center",
                "notifications_center is defined.")
        except Exception:
            nc = None
            log("browser/notifications_center",
                "notifications_center is missing.", "error")
        self.assertTrue(nc is not None)

        try:
            from eea.notifications.browser.notifications_center import \
                NotificationsCenter as nc
            log("browser/notifications_center",
                "NotificationsCenter is defined.")
        except Exception:
            nc = None
            log("browser/notifications_center",
                "NotificationsCenter is missing.", "error")
        self.assertTrue(nc is not None)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
