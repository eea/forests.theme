from Products.Five.browser import BrowserView


class MosaicTilesView(BrowserView):
    """ A fallback view for mosaic pages
    """

    def tiles(self):
        return getattr(self.context, 'tiles', {})
