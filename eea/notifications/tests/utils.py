# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile

import eea.notifications


def log(test_name, test_info, status="success"):
    class Color:
        OK = '\033[92m'
        ERR = '\033[91m'
        END = '\033[0m'

    text = "\n    TESTING {:>40}: {}".format(test_name, test_info)
    if status == "success":
        text = "{0}{1}{2}".format(Color.OK, text, Color.END)
    else:
        text = "{0}{1}{2}".format(Color.ERR, text, Color.END)

    print(text)


class NotificationsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=eea.notifications)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'eea.notifications:default')


NOTIFICATIONS_FIXTURE = NotificationsLayer()


NOTIFICATIONS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(NOTIFICATIONS_FIXTURE,),
    name='NotificationsLayer:IntegrationTesting'
)


NOTIFICATIONS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(NOTIFICATIONS_FIXTURE,),
    name='NotificationsLayer:FunctionalTesting'
)
