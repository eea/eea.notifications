from eea.notifications.tests.utils import log
import unittest


class TestNotifications(unittest.TestCase):

    def test_notifications(self):
        log("notifications", "send_email_notifications is defined.")

        from eea.notifications.notifications import send_email_notification

        self.assertTrue('function' in str(type(send_email_notification)))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
