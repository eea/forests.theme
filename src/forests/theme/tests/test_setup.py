# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from forests.theme.testing import FORESTS_THEME_INTEGRATION_TESTING  # noqa

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that forests.theme is properly installed."""

    layer = FORESTS_THEME_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if forests.theme is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'forests.theme'))

    def test_browserlayer(self):
        """Test that IForestsThemeLayer is registered."""
        from forests.theme.interfaces import (
            IForestsThemeLayer)
        from plone.browserlayer import utils
        self.assertIn(IForestsThemeLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = FORESTS_THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['forests.theme'])

    def test_product_uninstalled(self):
        """Test if forests.theme is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'forests.theme'))

    def test_browserlayer_removed(self):
        """Test that IForestsThemeLayer is removed."""
        from forests.theme.interfaces import IForestsThemeLayer
        from plone.browserlayer import utils
        self.assertNotIn(IForestsThemeLayer, utils.registered_layers())
