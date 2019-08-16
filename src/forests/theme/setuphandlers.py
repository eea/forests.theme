# -*- coding: utf-8 -*-

import json

from zope.interface import implementer

from plone import api
from Products.CMFPlone.interfaces import INonInstallable


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""

        return [
            'kitconcept.voltodemo:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # portal = api.portal.get()

    # create_default_homepage()


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def add_catalog_indexes(context, wanted=None):
    """Method to add our wanted indexes to the portal_catalog.
    """
    catalog = api.portal.get_tool('portal_catalog')
    indexes = catalog.indexes()
    indexables = []

    for name, meta_type in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)

    if len(indexables) > 0:
        catalog.manage_reindexIndex(ids=indexables)


def create_default_homepage():
    portal = api.portal.get()

    tiles = {}
    tiles_layout = []

    if not getattr(portal, 'tiles', False):
        portal.manage_addProperty('tiles', json.dumps(tiles), 'string')

    if not getattr(portal, 'tiles_layout', False):
        portal.manage_addProperty('tiles_layout', json.dumps(tiles_layout),
                                  'string')  # noqa

    portal.setTitle('Welcome to Forsts!')
    portal.setDescription('The Forests Information System for Europe')
