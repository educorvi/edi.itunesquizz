# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from edi.itunesquizz.testing import EDI_ITUNESQUIZZ_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that edi.itunesquizz is properly installed."""

    layer = EDI_ITUNESQUIZZ_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if edi.itunesquizz is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'edi.itunesquizz'))

    def test_browserlayer(self):
        """Test that IEdiItunesquizzLayer is registered."""
        from edi.itunesquizz.interfaces import (
            IEdiItunesquizzLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IEdiItunesquizzLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = EDI_ITUNESQUIZZ_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['edi.itunesquizz'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if edi.itunesquizz is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'edi.itunesquizz'))

    def test_browserlayer_removed(self):
        """Test that IEdiItunesquizzLayer is removed."""
        from edi.itunesquizz.interfaces import \
            IEdiItunesquizzLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IEdiItunesquizzLayer,
            utils.registered_layers())
