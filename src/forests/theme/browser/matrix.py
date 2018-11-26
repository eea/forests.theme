from Products.Five import BrowserView
from xlrd import open_workbook
import json
from zope.annotation import IAnnotations
from zope.component.hooks import getSite


class ImportMatrixData(BrowserView):
    """ Matrix data import
    """

    def __call__(self):
        context = self.context
        site = getSite()
        anno = IAnnotations(site)
        #anno.setDefault('matrix', {})
        anno['matrix'] = {}
        if not anno.get('matrix'):
            anno['matrix'] = {}
        matrix = anno.get('matrix')
        mfile = context.restrictedTraverse('land-use-matrix-by-ms-from-2018-ghg-inventory-simple.xlsx')
        fcontents =  open_workbook(file_contents=mfile.file.data)
        sheet = fcontents.sheets()[0]
        from_last_key = {}
        for row in range(1, sheet.nrows):
            fromv  = sheet.cell(row, 1).value
            if not matrix.has_key(fromv):
                from_last_key[fromv] = 1
                matrix[fromv] = {}
            matrix_from = matrix[fromv]
            key = from_last_key[fromv]   
            matrix_from[key] = {}
            key_values = matrix_from[key]
            for col in range(sheet.ncols):
                title_column_value = sheet.cell(0,col).value
                if type(title_column_value) == float:
                    title_column_value = int(title_column_value)
                key_values[title_column_value] = sheet.cell(row, col).value
            from_last_key[fromv] += 1
        return "Ok"


class QueryMatrixData(BrowserView):

    def __call__(self):
        site = getSite()
        anno = IAnnotations(site)
        fromv = self.context.REQUEST.get('from')        
        bad_request = False
        matrix = anno.get('matrix')
        if not matrix  or not fromv:
            bad_request = True 
            results = {}
        if not bad_request:
            results = matrix.get(fromv, {})
        
        self.context.REQUEST.response.setHeader("Content-type", "application/json")

        return json.dumps(results)
