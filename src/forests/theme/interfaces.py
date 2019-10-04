# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope import schema
from zope.interface import Attribute, Interface, alsoProvides
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from forests.theme import _
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives, model
from z3c.formwidget.optgroup.widget import OptgroupFieldWidget


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


class IMetadata(model.Schema):
    """ Generic metadata for forests data types
    """

    directives.fieldset('fise-metadata', label="Forests Metadata", fields=[
        'resource_type',
        'data_source',
        'dataset',
        'publisher',
        'external_url',
        'geo_coverage',
        'publishing_year',
        'collection_year_start',
        'collection_year_end',
        'topics',
        'keywords',
        'info_level',
        'accessibility_level',
    ])

    resource_type = schema.Choice(
        title=u'Resource type', vocabulary="fise.resource_types")

    data_source = schema.Choice(
        title=u"Data Source",
        vocabulary="fise.data_sources"
    )
    form.widget(
        'data_source',
        OptgroupFieldWidget,
        vocabulary='fise.data_sources'
    )

    dataset = schema.Choice(title=u"Dataset", vocabulary="fise.datasets")

    publisher = schema.TextLine(title=u"Publisher")  # text with autocomplete
    form.widget(
        'publisher',
        AjaxSelectFieldWidget,
        vocabulary='fise.publishers'
    )

    external_url = schema.TextLine(title=u"Link to resource")

    geo_coverage = schema.Tuple(
        title=u"Geographical coverage",
        value_type=schema.Choice(vocabulary="fise.geocoverage"))

    publishing_year = schema.Int(title=u"Publishing year")

    # interval between 2 years
    collection_year_start = schema.TextLine(title=u"Collection start year")
    collection_year_end = schema.TextLine(title=u"Collection end year")

    topics = schema.Tuple(
        title=u"Topics",
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )
    form.widget(
        'topics',
        AjaxSelectFieldWidget,
        vocabulary='fise.topics'
    )

    keywords = schema.Tuple(
        title=u"Keywords",
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )
    form.widget(
        'keywords',
        AjaxSelectFieldWidget,
        vocabulary='fise.keywords'
    )

    info_level = schema.Choice(title=u"Info level",
                               values=('A', 'B', 'C', 'D', 'E'))

    accessibility_level = schema.Choice(title=u'Accesibility levels',
                                        vocabulary='fise.accessibility_levels')


class IOptionalMetadata(model.Schema):
    """ Generic optional metadata for forests data types
    """

    nuts_level = schema.Tuple(
        title=u"NUTS Levels",
        value_type=schema.Choice(
            vocabulary="fise.nuts_levels")
    )
    directives.fieldset('fise-metadata', label="Forests Metadata", fields=[
        'nuts_level',
    ])


class IComputedMetadata(Interface):
    """ Forests Metadata fields that are automatically computed
    """

    resource_format = Attribute(u'Extracted from file extension')


alsoProvides(IMetadata, IFormFieldProvider)
alsoProvides(IOptionalMetadata, IFormFieldProvider)
