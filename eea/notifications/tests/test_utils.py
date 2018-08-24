from eea.notifications.tests.utils import log
import unittest


class TestUtils(unittest.TestCase):

    def test_utils(self):
        try:
            from eea.notifications.utils import LOGGER
            log("utils", "LOGGER is defined.")
        except Exception:
            LOGGER = None
            log("utils", "LOGGER is missing.", "error")
        self.assertTrue(LOGGER is not None)

        try:
            from eea.notifications.utils import list_content_types
            log("utils", "list_content_types is defined.")
        except Exception:
            list_content_types = None
            log("utils", "list_content_types is missing.", "error")
        self.assertTrue(list_content_types is not None)

        try:
            from eea.notifications.utils import get_tags
            log("utils", "get_tags is defined.")
        except Exception:
            get_tags = None
            log("utils", "get_tags is missing.", "error")
        self.assertTrue(get_tags is not None)

        try:
            from eea.notifications.utils import get_rabbit_config
            log("utils", "get_rabbit_config is defined.")
        except Exception:
            get_rabbit_config = None
            log("utils", "get_rabbit_config is missing.", "error")
        self.assertTrue(get_rabbit_config is not None)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
