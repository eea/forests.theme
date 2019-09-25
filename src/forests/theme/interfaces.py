# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from forests.theme import _
from plone.autoform import directives as form
from plone.supermodel import model


class IForestsThemeLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IMosaicSettings(model.Schema):
    """ Settings for mosaic tiles
    """

    form.widget(styles='z3c.form.browser.textlines.TextLinesFieldWidget')
    styles = schema.Set(
        title=_(u'Styles'),
        description=_(
            u'Enter a list of styles to appear in the style pulldown. '
            u'Format is title|className, one per line.'),
        required=False,
        default=set(["default|default-tile", ]),
        value_type=schema.ASCIILine(title=_(u'CSS Classes')),
    )
