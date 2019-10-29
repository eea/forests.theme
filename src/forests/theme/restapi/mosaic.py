from zope.component import getUtility  # adapter, getMultiAdapter

from forests.theme.interfaces import IMosaicSettings
from plone.registry.interfaces import IRegistry
from plone.restapi.services import Service


class MosaicSettingsGet(Service):
    """ Get the mosaic settings
    """

    def reply(self):
        proxy = getUtility(IRegistry).forInterface(IMosaicSettings)

        return {
            'styles': list(proxy.styles)
        }
