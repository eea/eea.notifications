# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile

import eea.notifications


class NotificationsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=eea.meeting)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'eea.meeting:default')


NOTIFICATIONS_FIXTURE = NotificationsLayer()


NOTIFICATIONS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(NOTIFICATIONS_FIXTURE,),
    name='NotificationsLayer:IntegrationTesting'
)


NOTIFICATIONS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(NOTIFICATIONS_FIXTURE,),
    name='NotificationsLayer:FunctionalTesting'
)
