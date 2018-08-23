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
        except Exception:
            catalog = None

        if catalog is not None:
            log("test_catalogtool", "Custom catalog exists.")
        else:
            log("test_catalogtool", "Custom catalog is missing.", "error")


class TestCatalogTool(unittest.TestCase):

    def test_catalogtool(self):
        log("test_catalogtool", "get_catalog function exists.")

        from eea.notifications.catalogtool import get_catalog
        self.assertTrue('function' in str(type(get_catalog)))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
