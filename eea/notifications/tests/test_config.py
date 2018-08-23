from eea.notifications.tests.utils import log
import unittest


class TestConfig(unittest.TestCase):

    def test_env_vars(self):
        log("config", "Non empty env vars in configuration.")

        from eea.notifications.config import ENV_HOST_NAME
        from eea.notifications.config import ENV_PLONE_NAME
        from eea.notifications.config import ANNOT_TAGS_KEY
        from eea.notifications.config import ANNOT_EVENTS_KEY
        from eea.notifications.config import OBJECT_EVENTS
        from eea.notifications.config import RABBIT_QUEUE

        self.assertTrue(ENV_HOST_NAME)
        self.assertTrue(ENV_PLONE_NAME)
        self.assertTrue(ANNOT_TAGS_KEY)
        self.assertTrue(ANNOT_EVENTS_KEY)
        self.assertTrue(OBJECT_EVENTS)
        self.assertTrue(RABBIT_QUEUE)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
