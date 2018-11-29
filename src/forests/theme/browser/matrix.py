from Products.Five import BrowserView
from xlrd import open_workbook
import json
from zope.annotation import IAnnotations
from zope.component.hooks import getSite
from collections import OrderedDict


class ImportMatrixData(BrowserView):
    """ Matrix data import
    """

    def __call__(self):
        context = self.context
        if 'land-matrix' not in context.getId():
            return "View should be called on the matrix excel file"
        site = getSite()
        anno = IAnnotations(site)
        sheet_number = 0
        fcontents =  open_workbook(file_contents=context.file.data)
        for sheet in fcontents.sheets():
            sheet_name = 'matrix_%s' % sheet_number
            matrix = anno.get(sheet_name)
            if not matrix:
               anno[sheet_name] = OrderedDict()
               matrix = anno[sheet_name]
            matrix['header'] = []
            for i in range(sheet.ncols):
                matrix['header'].append(sheet.cell(0, i).value)
            for row in range(1, sheet.nrows):
                fromv  = sheet.cell(row, sheet_number).value
                if not matrix.has_key(fromv):
                    matrix[fromv] = []
                matrix_list = matrix[fromv]
                row_values = []
                for col in range(sheet.ncols):
                    row_values.append(sheet.cell(row, col).value)
                matrix_list.append(row_values)
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

    @staticmethod
    def get_table_data():
        site = getSite()
        anno = IAnnotations(site)
        matrix = anno.get('matrix_0')
        results_list = []
        i = 0;
        for value in matrix.values():
            if i == 0:
                results_list.append(value)
            else:
                results_list.append(value[0])
            i += 1
        return results_list
