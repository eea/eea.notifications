from eea.notifications.tests.utils import log
import unittest


class TestInterfaces(unittest.TestCase):

    def test_interfaces(self):
        try:
            from eea.notifications.interfaces import \
                    IEEANotificationsCatalogTool
            log("interfaces", "IEEANotificationsCatalogTool is defined.")
        except Exception:
            IEEANotificationsCatalogTool = None
            log("interfaces",
                "IEEANotificationsCatalogTool is missing.", "error")
        self.assertTrue(IEEANotificationsCatalogTool is not None)

        try:
            from eea.notifications.interfaces import IEEANotificationsInstalled
            log("interfaces", "IEEANotificationsInstalled is defined.")
        except Exception:
            IEEANotificationsInstalled = None
            log("interfaces",
                "IEEANotificationsInstalled is missing.", "error")
        self.assertTrue(IEEANotificationsInstalled is not None)

        try:
            from eea.notifications.interfaces import IPingRMQAction
            log("interfaces", "IPingRMQAction is defined.")
        except Exception:
            IPingRMQAction = None
            log("interfaces", "IPingRMQAction is missing.", "error")
        self.assertTrue(IPingRMQAction is not None)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
