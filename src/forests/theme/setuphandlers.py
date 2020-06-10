# -*- coding: utf-8 -*-
''' setuphandlers module '''

import json

from zope.interface import implementer

from plone import api
from Products.CMFPlone.interfaces import INonInstallable


@implementer(INonInstallable)
class HiddenProfiles(object):
    """HiddenProfiles."""

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""

        return [
            'forests.theme:uninstall',
            'forests.theme:content',
        ]


def post_install(context):
    """Post install script"""

    create_default_homepage()


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

    if indexables:
        catalog.manage_reindexIndex(ids=indexables)


def create_default_homepage():
    """create_default_homepage."""
    portal = api.portal.get()

    tiles = {
        "0358abe2-b4f1-463d-a279-a63ea80daf19": {
            "@type": "description"
        },
        "07c273fc-8bfc-4e7d-a327-d513e5a945bb": {
            "@type": "title"
        },
        "2dfe8e4c-5bf6-43f1-93e1-6c320ede7226": {
            "@type": "text",
            "text": {
                "blocks": [
                    {
                        "data": {},
                        "depth": 0,
                        "entityRanges": [],
                        "inlineStyleRanges": [
                            {
                                "length": 10,
                                "offset": 0,
                                "style": "BOLD"
                            }
                        ],
                        "key": "6470b",
                        "text": "Fill in text here",
                        "type": "unstyled"
                    }
                ],
                "entityMap": {}
            }
        },
    }

    tiles_layout = [
        "0358abe2-b4f1-463d-a279-a63ea80daf19",
        "07c273fc-8bfc-4e7d-a327-d513e5a945bb",
        "2dfe8e4c-5bf6-43f1-93e1-6c320ede7226"
    ]

    if not getattr(portal, 'tiles', False):
        portal.manage_addProperty('tiles', json.dumps(tiles), 'string')

    if not getattr(portal, 'tiles_layout', False):
        portal.manage_addProperty('tiles_layout', json.dumps(tiles_layout),
                                  'string')  # noqa

    portal.setTitle('Welcome to Forests!')
    portal.setDescription('The Forests Information System for Europe')
