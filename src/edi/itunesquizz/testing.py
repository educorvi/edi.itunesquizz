# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import edi.itunesquizz


class EdiItunesquizzLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=edi.itunesquizz)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'edi.itunesquizz:default')


EDI_ITUNESQUIZZ_FIXTURE = EdiItunesquizzLayer()


EDI_ITUNESQUIZZ_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EDI_ITUNESQUIZZ_FIXTURE,),
    name='EdiItunesquizzLayer:IntegrationTesting',
)


EDI_ITUNESQUIZZ_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EDI_ITUNESQUIZZ_FIXTURE,),
    name='EdiItunesquizzLayer:FunctionalTesting',
)


EDI_ITUNESQUIZZ_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EDI_ITUNESQUIZZ_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='EdiItunesquizzLayer:AcceptanceTesting',
)
