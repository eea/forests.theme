# -*- coding: utf-8 -*-
""" Module where all interfaces, events and exceptions live.
"""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface


class IForestsThemeLayer(IDefaultBrowserLayer):
    """ Marker interface that defines a browser layer.
    """


class ILocalSectionMarker(Interface):
    """ A local section marker. To be used with @localnavigation.
        BBB - now registered under eea.restapi
    """