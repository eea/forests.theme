from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ForestsSectionsViewlet(GlobalSectionsViewlet):
    index = ViewPageTemplateFile('pt/navbar-viewlet.pt')

    def update(self):
        pass
