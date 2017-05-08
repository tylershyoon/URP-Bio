# -*- coding: cp949 -*-

import xlrd
import tools

def excel_retrieve(filename):
    wb = xlrd.open_workbook(filename)
    #print wb.sheet_names()

    # Selecting sheet, the first one
    ws = wb.sheet_by_index(0)
    nrows = ws.nrows

    row_val = []
    for row_num in range(nrows):
        print ws.row_values((row_num))
        row_val.append(ws.row_values(row_num))
    return_lst = tools.encode_lst(row_val)
    # PRINT LST
    #tools.print_lst(return_lst)
    ALU_in_3UTR_names = [elem for elem in return_lst]
    print ALU_in_3UTR_names
    return return_lst





excel_retrieve('emboj200894s3.xls')
