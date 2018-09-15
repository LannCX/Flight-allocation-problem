# -*- coding: utf-8 -*-
import os,xlrd
import xlwt
from datetime import date, datetime
root_dir = '..'

def read_excel():
    # 打开文件
    workbook = xlrd.open_workbook(os.path.join(root_dir,'InputData.xlsx'))
    # 获取所有sheet
    print(workbook.sheet_names() )
    sheet2_name = workbook.sheet_names()[1]

    # 根据sheet索引或者名称获取sheet内容
    sheet2 = workbook.sheet_by_index(0)  # sheet索引从0开始
    sheet2 = workbook.sheet_by_name(sheet2_name)

    # sheet的名称，行数，列数
    print(sheet2.name, sheet2.nrows, sheet2.ncols)

    # 获取整行和整列的值（数组）
    rows = sheet2.row_values(3)  # 获取第四行内容
    cols = sheet2.col_values(3)  # 获取第三列内容
    print(rows)
    print(cols)

    # 获取单元格内容
    print(sheet2.cell(1, 0).value.encode('utf-8'))
    print(sheet2.cell_value(1, 0).encode('utf-8'))
    print(sheet2.row(1)[0].value.encode('utf-8'))

    # 获取单元格内容的数据类型
    if (sheet2.cell(1, 3).ctype == 3):
        date_value = xlrd.xldate_as_tuple(sheet2.cell_value(1, 3), workbook.datemode)
        date_tmp = date(*date_value[:3]).strftime('%Y-%m-%d')
        print(date_tmp)

if __name__ == '__main__':
    read_excel()