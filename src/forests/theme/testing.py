# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import pas.plugins.ldap
import yafowil.plone
import forests.theme


class ForestsThemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=yafowil.plone)
        self.loadZCML(package=pas.plugins.ldap)
        self.loadZCML(package=forests.theme)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'forests.theme:default')


FORESTS_THEME_FIXTURE = ForestsThemeLayer()


FORESTS_THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FORESTS_THEME_FIXTURE,),
    name='ForestsThemeLayer:IntegrationTesting'
)
