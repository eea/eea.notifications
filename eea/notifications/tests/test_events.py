from eea.notifications.tests.utils import log
import unittest


class TestEvents(unittest.TestCase):

    def test_events(self):
        try:
            from eea.notifications.actions.events import \
                add_or_update_in_catalog
            from eea.notifications.actions.events import remove_from_catalog
            from eea.notifications.actions.events import object_modified
            from eea.notifications.actions.events import object_moved
            from eea.notifications.actions.events import object_added
            from eea.notifications.actions.events import object_removed
            log("actions/events", "Events defined.")
        except Exception:
            add_or_update_in_catalog = None
            remove_from_catalog = None
            object_modified = None
            object_moved = None
            object_added = None
            object_removed = None
            log("actions/events", "Events missing.", "error")
        self.assertTrue(add_or_update_in_catalog is not None)
        self.assertTrue(remove_from_catalog is not None)
        self.assertTrue(object_modified is not None)
        self.assertTrue(object_moved is not None)
        self.assertTrue(object_added is not None)
        self.assertTrue(object_removed is not None)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
