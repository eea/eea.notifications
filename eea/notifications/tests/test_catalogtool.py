from eea.notifications.tests.utils import log
import unittest


class TestCatalogTool(unittest.TestCase):

    def test_catalogtool(self):
        log("test_catalogtool", "get_catalog function exists.")

        from eea.notifications.catalogtool import get_catalog
        self.assertTrue('function' in str(type(get_catalog)))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
