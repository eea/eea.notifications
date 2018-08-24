from eea.notifications.tests.utils import log
import unittest


class TestIndexers(unittest.TestCase):

    def test_indexers(self):
        try:
            from eea.notifications.content.indexers import getTags
            log("content/indexers", "getTags is defined.")
        except Exception:
            getTags = None
            log("content/indexers", "getTags is missing.", "error")
        self.assertTrue(getTags is not None)

        try:
            from eea.notifications.content.indexers import getUserTags
            log("content/indexers", "getUserTags is defined.")
        except Exception:
            getUserTags = None
            log("content/indexers", "getUserTags is missing.", "error")
        self.assertTrue(getUserTags is not None)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
