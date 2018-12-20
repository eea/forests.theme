from Products.Five import BrowserView
from xlrd import open_workbook
import json
from zope.annotation import IAnnotations
from zope.component.hooks import getSite
from collections import OrderedDict


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

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
        fcontents = open_workbook(file_contents=context.file.data)
        for sheet in fcontents.sheets():
            sheet_name = 'matrix_%s' % sheet_number
            matrix = anno.get(sheet_name)
            if matrix:
                anno.pop(sheet_name)
                anno[sheet_name] = OrderedDict()
                matrix = anno[sheet_name]
            else:
                anno[sheet_name] = OrderedDict()
                matrix = anno[sheet_name]
            matrix['header'] = []
            for i in range(sheet.ncols):
                # datatable needs it's heading values to be string as such
                # each header value is converted to string
                matrix['header'].append(str(sheet.cell(0, i).value))
            for row in range(1, sheet.nrows):
                fromv = sheet.cell(row, sheet_number).value
                if fromv not in matrix:
                    matrix[fromv] = []
                matrix_list = matrix[fromv]
                row_values = []
                for col in range(sheet.ncols):
                    cell_value = sheet.cell(row, col).value
                    if type(cell_value) == float:
                        cell_value = truncate(cell_value, 4)
                    row_values.append(cell_value)
                matrix_list.append(row_values)
            sheet_number += 1

        # select categories import, if it runs within a different browserview
        # then the data saved from this logic isn't persisted
        form = self.context.REQUEST.form
        num_of_rows = form.get('num_of_rows', 3)
        matrix = anno["matrix_1"]
        anno["matrix_1"]['select_categories'] = OrderedDict()
        header_values = matrix['header'][0:num_of_rows]
        for value in header_values:
            matrix['select_categories'][value] = []
        matrix_keys = matrix.keys()
        select_categories_keys = matrix['select_categories'].keys()
        for key in matrix_keys[1:-1]:
            rows = matrix[key]
            for row in rows:
                for idx, single_row in enumerate(row[0:num_of_rows]):
                    category_list = anno["matrix_1"]['select_categories'][
                            select_categories_keys[idx]]
                    if single_row not in category_list:
                        category_list.append(single_row)
        return "Ok"


class QueryMatrixData(BrowserView):

    def __call__(self):
        site = getSite()
        anno = IAnnotations(site)
        form = self.context.REQUEST.form
        bad_request = False
        matrix = anno.get('matrix_1')
        results = {}
        if not matrix:
            bad_request = True 
        if not bad_request:
            fromv = form.get('From[]', matrix.keys()[1:-2])
            cleaned_form = {}
            for k,v in form.items():
                cleaned_form[k.split('[]')[0]] = v
            found = []
            select_criterias_keys = matrix['select_categories'].keys()
            fromv = [fromv] if not isinstance(fromv, list) else fromv
            criterias = cleaned_form.items()
            criterias_len = len(criterias)
            for value in fromv:
                rows = matrix.get(value, [])
                for row in rows:
                    matched_criterias = 0
                    for k, v in criterias:
                        index = select_criterias_keys.index(k)
                        if isinstance(v, list):
                            for entry in v:
                                if row[index] == entry:
                                    matched_criterias += 1
                                    break
                        else:
                            if row[index] == v:
                                matched_criterias += 1
                        if criterias_len == matched_criterias:
                            found.append(row)
            cdefs = matrix['header']
            results['columnDefs'] = cdefs
            results['data'] = found
        self.context.REQUEST.response.setHeader("Content-type",
                                                "application/json")
        return json.dumps(results)

    @staticmethod
    def get_table_data():
        site = getSite()
        anno = IAnnotations(site)
        matrix = anno.get('matrix_0')
        results_list = []
        i = 0
        for value in matrix.values():
            if i == 0:
                results_list.append(value)
            else:
                results_list.append(value[0])
            i += 1
        return results_list

    @staticmethod
    def get_table_filters():
        site = getSite()
        anno = IAnnotations(site)
        matrix = anno.get('matrix_1', {})
        return matrix.get('select_categories', {})
