
from forests.theme.browser.site import _extract_menu
from plone.directives import form
from plone.memoize import view
from zope import schema
from z3c.form import button
from Products.CMFCore.utils import getToolByName
from zope.interface import (Invalid, invariant)


class InvalidMenuConfiguration(Invalid):
    __doc__ = u"The menu format is invalid"


class IMainNavigationMenu(form.Schema):
    menu = schema.Text(title=u"Menu structure text", required=True)

    @invariant
    def check_menu(data):
        try:
            _extract_menu(data.menu)
        except Exception, e:
            raise InvalidMenuConfiguration(e)


class MainNavigationMenuEdit(form.SchemaForm):
    """ A page to edit the main site navigation menu
    """

    schema = IMainNavigationMenu
    ignoreContext = False

    label = u"Fill in the content of the main menu"
    description = u"""This should be a structure for the main menu. Use a single
    empty line to separate main menu entries. All lines after the main menu
    entry, and before an empty line, will form entries in that section menu. To
    create a submenu for a section, start a line with a dash (-).  Links should
    start with a slash (/)."""

    @property
    def ptool(self):
        return getToolByName(self.context,
                             'portal_properties')['site_properties']

    @view.memoize
    def getContent(self):
        content = {'menu': self.ptool.getProperty('main_navigation_menu')}

        return content

    @button.buttonAndHandler(u"Save")
    def handleApply(self, action):
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage

            return

        self.ptool._updateProperty('main_navigation_menu', data['menu'])

        self.status = u"Saved, please check."
