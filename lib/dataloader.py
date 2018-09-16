import os,xlrd
import xlwt
import numpy as np
from datetime import date, datetime

root_dir = '..'
# 宽窄机型对照表
aircraft = {'W':['332','333','33E','33H','33L','773'],
            'N':['319','320','321','323','325','738','73A','73E','73H','73L']}

# 旅客最短流程表(到达(a)/出发(l)、国内(D)/国际(I)、航站楼(T)/卫星厅(S))
flow = [[15,20,35,40],[20,15,40,35],[35,40,20,30],[40,45,30,20]]
count = [[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,2,1,0]]

# 字典格式输出Pucks、Tickets、Gates三个表格
def read_data():
    # 打开文件
    workbook = xlrd.open_workbook(os.path.join(root_dir,'InputData.xlsx'))

    # Get Pucks
    Pucks = {}
    sheet = workbook.sheet_by_name('Pucks')
    for i in range(1,sheet.nrows):
        key = sheet.cell_value(i,0)
        dic = {}  # 字典内字典
        for j in range(1,sheet.ncols):
            if sheet.cell(i, j).ctype == 3:
                # 到达、出发日期
                if j== 1 or j==6:
                    data_value = xlrd.xldate_as_tuple(sheet.cell_value(i,j), workbook.datemode)
                    val = date(*data_value[:3]).strftime('%Y-%m-%d')
                # 到达、出发时间
                elif j==2 or j==7:
                    data_value = xlrd.xldate_as_tuple(sheet.cell_value(i, j), workbook.datemode)
                    val = str(data_value[-3]).zfill(2) + ':' + str(data_value[-2]).zfill(2)
                else:
                    pass
            # 飞机型号(部分为float，改为str)
            elif sheet.cell(i, j).ctype == 2:
                val = str(int(sheet.cell_value(i,j)))
            else:
                val = sheet.cell(i,j).value
            dic[sheet.cell(0, j).value.replace('\n','')] = val
        Pucks[key] = dic

    # Get Tickets
    Tickets = {}
    sheet = workbook.sheet_by_name('Tickets')
    for i in range(1, sheet.nrows):
        key = sheet.cell_value(i, 0)
        dic = {}  # 字典内字典
        for j in range(1, sheet.ncols):
            if sheet.cell(i, j).ctype == 3:
                # 到达、出发日期
                if j == 3 or j == 5:
                    data_value = xlrd.xldate_as_tuple(sheet.cell_value(i, j), workbook.datemode)
                    val = date(*data_value[:3]).strftime('%Y-%m-%d')
                else:
                    pass
            else:
                val = sheet.cell(i, j).value
            dic[sheet.cell(0, j).value.replace('\n', '')] = val
        Tickets[key] = dic

    # Get Gates
    Gates = {}
    sheet = workbook.sheet_by_name('Gates')
    for i in range(1, sheet.nrows):
        key = sheet.cell_value(i, 0)
        dic = {}  # 字典内字典
        for j in range(1, sheet.ncols):
            val = sheet.cell(i, j).value
            dic[sheet.cell(0, j).value.replace('\n', '')] = val
        Gates[key] = dic

    return Pucks, Tickets, Gates

# 登机口数据预处理
def data_filter(pucks):
    remove_list = []
    # 遍历字典
    for key,value in pucks.items():
        # 删除与20号没有交集的航班
        if '2018-01-20' not in [value['到达日期'], value['出发日期']]:
            remove_list.append(key)
            continue

        # 航班离开时刻加45分钟(总的飞机停留时间段)
        time = [int(x) for x in value['出发时刻'].split(':')]
        if time[1]+45>=60:
            time[1] = time[1]+45-60
            time[0] += 1
            if time[0]>24:
                time[0]=24
                time[1]=0
        else:
            time[1] +=45

        value['出发时刻'] = str(time[0]).zfill(2) + str(time[1]).zfill(2)
        # 统一航班到达时刻时间格式
        time = [int(x) for x in value['到达时刻'].split(':')]
        value['到达时刻'] = str(time[0]).zfill(2) + str(time[1]).zfill(2)

        # 考虑隔天停留（19到达20号离开、20号到达21号离开）
        if value['到达日期'] == '2018-01-19':
            value['到达时刻'] = '0000'
        elif value['出发日期'] == '2018-01-21':
            value['出发时刻'] = '2400'
    for k in remove_list:
        pucks.pop(k)

    return pucks

# 统计每个航班的人数（带星号航班不考虑）
def calc_passenger(tickets):
    table = {}
    # 遍历字典
    for key, value in tickets.items():
        pass
    return table

if __name__ == '__main__':
    P, T, G = read_data()
    Pucks = data_filter(P)
    t = calc_passenger(T)