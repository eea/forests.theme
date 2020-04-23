""" Views useful for the entire website functionality
"""

import logging
import re

from hashlib import md5
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.PythonScripts.standard import url_quote
from time import time
from zope.component.hooks import getSite


LINKER = re.compile('(?P<icon>\[.+?\])(?P<label>.+)')

logger = logging.getLogger('forests.theme')

# NOTICE: you don't have to edit the menu here. This is a fallback, the menu
# is rendered live, from information stored in the portal. Use to edit:
# https://demo-forests.eea.europa.eu/@@edit-navigation-menu
DEFAULT_MENU = """
Topics /topics

Data and maps /data-and-maps

Indicators /indicators

Countries and regions /countries-and-regions
  Countries /countries-and-regions
    -Albania /countries-and-regions/albania
    -Austria /countries-and-regions/austria
    -Belgium /countries-and-regions/belgium
  See all countries /countries-and-regions
  Regions /countries-and-regions
    -Eu28 /countries-and-regions/eu28
    -Eu39 /countries-and-regions/eu39
  See all regions /countries-and-regions

Tools /tools    """


class MenuParser:
    EMPTY_LINE = 'EMPTY_LINE'
    SECTION_SEPARATOR = 'SECTION_SEPARATOR'
    ITEM = 'ITEM'
    SUBITEM = 'SUBITEM'
    site_url = None

    def __init__(self, site_url):
        self.site_url = site_url

    def _get_list_item(self, line):
        item = self._make_section()
        icon = ''
        label, link = line.split('/', 1)
        match = LINKER.match(label)

        if match:
            icon = match.group('icon').replace('[', '').replace(']', '')
            label = match.group('label').replace('[', '').replace(']', '')

        item.update({
            'icon': icon.strip(),
            'label': label.strip(),
            'link': self.site_url + '/' + link.strip(),
        })

        return item

    def _make_section(self,):
        return {
            'label': '',
            'link': '',
            'icon': '',
            'children': [],
        }

    def parse(self, text):
        value = text.strip()
        lines = value.split('\n')
        lines = [l.strip() for l in lines]

        self.reset()
        self.out = []

        for line in lines:
            self.process(line)

        # handle end of lines
        self.out.append(self.c_column)

        return self.out

    def process(self, line):
        token, payload = self.tokenize(line)
        handler = getattr(self, 'handle_' + token)
        handler(payload)

    def tokenize(self, line):
        line = line.strip()

        if not line:
            return (self.EMPTY_LINE, '')

        if line == '---':
            return (self.SECTION_SEPARATOR, '')

        token = self.ITEM

        if line.startswith('-'):
            token = self.SUBITEM
            line = line[1:]

        item = self._get_list_item(line)

        return (token, item)

    def handle_EMPTY_LINE(self, payload):
        # on empty lines, add the section and reset the state machine

        self.out.append(self.c_column)
        self.c_column = None
        self.reset()

    def handle_ITEM(self, item):
        if not self.c_column:           # this is a main section
            item['children'] = [[]]     # prepare the columns
            self.c_column = item
        else:
            self.c_group = item
            self.c_column['children'][-1].append(self.c_group)

    def handle_SUBITEM(self, item):
        self.c_group['children'].append(item)

    def handle_SECTION_SEPARATOR(self, payload):
        self.c_column['children'].append([])

    def reset(self):
        self.c_column = None


def _extract_menu(value, site_url=None):
    """ Construct the data for the menu.
    Terminology in the menu:
    |-----------------------------------------------------------|
    | <section>        |       <section>        |     <section> |
    |-----------------------------------------------------------|
    | <subsection>   <subsection>   |                           |
    | <group A>      <group C>      |                           |
    | <link 1>       <link 1>       |                           |
    | <link 2>       <link 2>       |                           |
    | ...                           |                           |
    | <group B>                     |                           |
    | <link 3>                      |                           |
    | <link 4>                      |                           |
    |-----------------------------------------------------------|
    """
    if not site_url:
        site_url = getSite().absolute_url()
    parser = MenuParser(site_url)
    result = parser.parse(value)

    return result


class Navbar(BrowserView):
    """ The global site navbar
    """

    def pp(self, v):
        import pprint

        return pprint.pprint(v)

    def menu(self):
        site_url = self.context.portal_url()
        try:
            ptool = getToolByName(self.context,
                                  'portal_properties')['site_properties']

            return _extract_menu(ptool.getProperty('main_navigation_menu'),
                                 site_url)
        except Exception as e:
            logger.exception("Error while rendering navigation menu: %s", e)
            return _extract_menu(DEFAULT_MENU, site_url)


class ExternalResourcesView(BrowserView):
    """ The global site navbar
    """
    def registry(self, name=None):
        name = name or 'css'
        return getToolByName(aq_inner(self.context), 'portal_' + name)

    def skinname(self):
        return aq_inner(self.context).getCurrentSkinName()

    def generateId(self, resource, other=None):
        """Generate a random id."""
        res_id = resource.getId()
        filename_appendix = '.css'

        if other is not None:
            other_id = other.getId()
            key = md5(other_id)
            key.update(res_id)
            base = res_id.rsplit('-')[0]
            key = "%s-" % (base, key.hexdigest())
            ext = "." + res_id.rsplit('.', 1)[1]
        else:
            base = res_id.replace('++', '').replace('/', '').rsplit('.', 1)[0]
            key = md5(res_id)
            key.update(str(int(time() * 1000)))
            key = "%s-cachekey-%s" % (base, key.hexdigest())
            ext = filename_appendix

        return key + ext

    def cook_resources(self, resource_type=None, bundle=None):
        bundle_id = bundle or 'external_templates'
        tool = self.registry(name=resource_type)
        results = []
        # concatenatedResources = {}
        resources = [r.copy() for r in tool.getResources() if
                     r.getEnabled() and r.getBundle() in [bundle_id]]
        for resource in resources:
            if resource.getCookable() or resource.getCacheable():
                # magic_id = self.generateId(resource)
                # concatenatedResources[magic_id] = [resource.getId()]
                magic_id = resource.getId()
                resource._setId(magic_id)
            results.append(resource)
        return tuple(results)

    def styles(self):
        # import pdb; pdb.set_trace()
        styles = self.cook_resources(resource_type='css')
        registry = self.registry()
        registry_url = registry.absolute_url()
        skinname = url_quote(self.skinname())
        result = []
        for style in styles:
            rendering = style.getRendering()
            src = "%s/%s/%s" % (registry_url, skinname, style.getId())
            data = {'rendering': rendering,
                    'media': style.getMedia(),
                    'rel': style.getRel(),
                    'title': style.getTitle(),
                    'conditionalcomment': style.getConditionalcomment(),
                    'src': src}
            result.append(data)
        return result

    def scripts(self):
        registry = self.registry(name='javascripts')
        registry_url = registry.absolute_url()
        # context = aq_inner(self.context)

        # scripts = registry.getEvaluatedResources(context)
        scripts = self.cook_resources(resource_type='javascripts')
        skinname = url_quote(self.skinname())
        result = []
        for script in scripts:
            src = "%s/%s/%s" % (registry_url, skinname, script.getId())
            data = {'inline': False,
                    'conditionalcomment': script.getConditionalcomment(),
                    'src': src}
            result.append(data)
        return result
