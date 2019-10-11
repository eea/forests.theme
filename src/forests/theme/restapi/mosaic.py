from zope.component import getUtility  # adapter, getMultiAdapter

from forests.theme.interfaces import IMosaicSettings
from plone.registry.interfaces import IRegistry
# from plone.restapi.batching import HypermediaBatch
# from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service

# from zope.interface import implementer
# from zope.publisher.interfaces import IRequest


# from plone.restapi.types.interfaces import IJsonSchemaProvider


class MosaicSettingsGet(Service):
    """ Get the mosaic settings
    """

    def reply(self):
        proxy = getUtility(IRegistry).forInterface(IMosaicSettings)

        return {
            'styles': list(proxy.styles)
        }

        # serializer = getMultiAdapter(
        #     (proxy, self.request), interface=ISerializeToJson
        # )
        # id = "{}/@mosaic-settings".format(
        #     self.context.absolute_url()
        # )
        #
        # serializer = SerializeRecordToJson(proxy)
        #
        # return serializer(id)


# class SerializeRecordToJson(object):
#     """ Simple serializer for a record, modeled after
#     plone/restapi/serializer/registry.py
#     """
#
#     def __init__(self, record):
#         self.record = record
#
#     def __call__(self, id):
#         # Batch keys, because that is a simple BTree
#
#         import pdb
#         pdb.set_trace()
#         record = self.record
#         results = {}
#         results["@id"] = id
#
#         def make_item(key):
#             schema = getMultiAdapter(
#                 (record.field, record, self.request), IJsonSchemaProvider
#             )
#             data = {"name": key, "value": self.registry[key]}
#             __traceback_info__ = (record, record.field, schema)
#             data["schema"] = {"properties": schema.get_schema()}
#
#             return data
#
#         results["items"] = [make_item(key) for key in batch]
#
#         return results

