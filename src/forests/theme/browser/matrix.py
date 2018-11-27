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
        if 'land-matrix' not in context.getId():
            return "View should be called on the matrix excel file"
        site = getSite()
        anno = IAnnotations(site)
        sheet_number = 1
        fcontents =  open_workbook(file_contents=context.file.data)
        from_last_key = {}
        for sheet in fcontents.sheets():
            sheet_name = 'matrix_%s' % sheet_number
            matrix = anno.get(sheet_name)
            if not matrix:
                anno[sheet_name] = {}
            for row in range(1, sheet.nrows):
                fromv  = sheet.cell(row, 1).value
                if not from_last_key.has_key(fromv):
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
            sheet_number += 1
        return "Ok"


class QueryMatrixData(BrowserView):

    def __call__(self):
        site = getSite()
        anno = IAnnotations(site)
        form = self.context.REQUEST.form
        fromv = form.get('From')        
        bad_request = False
        matrix = anno.get('matrix_1')
        results = {}
        if not matrix  or not fromv:
            bad_request = True 
        if not bad_request:
            form_keys = form.keys()
            results = matrix.get(fromv, {}).copy()
            for k,v in form.items():
                if k != 'From':
                    for key, value in results.items():
                        item_category = value.get(k)
                        if item_category and item_category != v:
                            del results[key] 
        
        self.context.REQUEST.response.setHeader("Content-type", 
                                                "application/json")

        return json.dumps(results)
