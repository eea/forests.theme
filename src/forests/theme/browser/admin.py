''' admin module '''

from forests.theme.browser.site import _extract_menu
from plone.directives import form
from plone.memoize import view
from zope import schema
from zope.interface import (Invalid, invariant)
from z3c.form import button
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView


class InvalidMenuConfiguration(Invalid):
    """InvalidMenuConfiguration."""

    __doc__ = u"The menu format is invalid"


class IMainNavigationMenu(form.Schema):
    """IMainNavigationMenu."""

    menu = schema.Text(title=u"Menu structure text", required=True)

    @invariant
    def check_menu(self, data):
        """check_menu.

        :param data:
        """
        try:
            _extract_menu(data.menu)
        except Exception as e:
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
        """ptool."""
        return getToolByName(self.context,
                             'portal_properties')['site_properties']

    @view.memoize
    def getContent(self):
        """getContent."""
        content = {'menu': self.ptool.getProperty('main_navigation_menu')}

        return content

    @button.buttonAndHandler(u"Save")
    def handleApply(self, action):
        """handleApply.

        :param action:
        """
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage

            return

        self.ptool._updateProperty('main_navigation_menu', data['menu'])

        self.status = u"Saved, please check."


class GoPDB(BrowserView):
    """pdb view
    """

    def __call__(self):
        # mtool = getToolByName(self.context, 'portal_membership')
        # has = mtool.checkPermission("Manage portal", self.context)

        # this code is helpful in debugging inheritance trees
        # pyflakes complains that it's unused, so we disable it here
        # enable if you need it
        # def classtree(cls, indent):
        #    """ method used in conjunction with instantree to display class
        #        tree
        #    """
        #  print '.'*indent, cls.__name__        # print class name here
        #  for supercls in cls.__bases__:        # recur to all superclasses
        #      classtree(supercls, indent+3)     # may visit super > once

        # def instancetree(inst):
        #    """ Helper method to recursively print all superclasses
        #    """
        #    print 'Tree of', inst                 # show instance
        #    classtree(inst.__class__, 3)          # climb to its class

        import pdb
        pdb.set_trace()

        return "Ok"
