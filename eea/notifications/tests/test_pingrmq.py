from eea.notifications.tests.utils import log
import unittest


class TestPingRMQ(unittest.TestCase):

    def test_pingrmq(self):
        try:
            from eea.notifications.actions.pingrmq import PingRMQAction
            from eea.notifications.actions.pingrmq import PingRMQActionExecutor
            from eea.notifications.actions.pingrmq import PingRMQAddForm
            from eea.notifications.actions.pingrmq import PingRMQEditForm
            log("actions/pingrmq", "Related items are defined.")
        except Exception:
            PingRMQAction = None
            PingRMQActionExecutor = None
            PingRMQAddForm = None
            PingRMQEditForm = None
            log("actions/pingrmq", "Related items are missing", "error")
        self.assertTrue(PingRMQAction is not None)
        self.assertTrue(PingRMQActionExecutor is not None)
        self.assertTrue(PingRMQAddForm is not None)
        self.assertTrue(PingRMQEditForm is not None)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
