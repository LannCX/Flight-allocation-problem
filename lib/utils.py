import pandas as pd
from lib import dataloader
import xlrd,xlwt
from xlutils.copy import copy

# 统计每个航班的人数（带星号航班不考虑）
# 输出table:{ 航班名：人数 }
def calc_passenger(pucks, tickets):
    table = {}
    # 遍历字典
    for pkey, pval in pucks.items():
        for tkey, tval in tickets.items():
            if pval['到达航班'] == tval['到达航班'] and pval['到达日期'] == tval['到达日期']:
                if pkey in table.keys():
                    table[pkey] = [tval['乘客数'], 0]
                else:
                    table[pkey][0] += tval['乘客数']
            else:
                pass

            if pval['出发航班'] == tval['出发航班'] and pval['出发日期'] == tval['出发日期']:
                if pkey in table.keys():
                    table[pkey] = [0,tval['乘客数']]
                else:
                    table[pkey][1] += tval['乘客数']
            else:
                pass

    return table

# 获取出入类型计算的系数
def getIta(stra,strb):
    '''
    :param stra: 行索引，字符串
    :param strb: 列索引，字符串
    :return: η值，整型
    '''
    dicRow = {'II':0,'ID':1,'IDI':2,'DI':3,'DD':4,'DDI':5,'DII':6,'DII':7,'DID':8,'DIDI':9}
    filePath = (r'InputData4.xlsx')
    data = pd.read_excel(filePath, encoding='gbk')
    res = data[stra][dicRow[strb]]
    return int(res)

# 旅客流程
def passengerFlow(stra,strb):
    '''
    数字a为表格InputData2.xlsx的列索引，数字b为其行索引
    :param a:表格索引{0:'DT',1:'DS',2:'IT',3:'IS'}
    :param b:表格索引{0:'DT',1:'DS',2:'IT',3:'IS'}
    :return:route：最短流程时间，cnt：捷运乘坐次数
    '''
    filePath = (r'../../InputData2.xlsx')
    data = pd.read_excel(filePath, encoding='gbk')
    # dict_temp = {0: 'DT', 1: 'DS', 2: 'IT', 3: 'IS'}
    dict_b = {'DT':0, 'DS':1, 'IT':2, 'IS':3}
    res = data[strb][dict_b[stra]]
    route = int(res[:2])
    cnt = int(res[-1])
    return route, cnt

#旅客行走时间，从登机口区域a走到b
def walkTime(stra,strb):
    '''
    :param a:表格索引{0:'T-North',1:'T-Center',2:'T-South',3:'S-North',4:'S-Center',5:'S-South',6:'S-East'}
    :param b:表格索引{0:'T-North',1:'T-Center',2:'T-South',3:'S-North',4:'S-Center',5:'S-South',6:'S-East'}
    :return:从登机口区域a走到b的时间
    '''
    filePath = (r'../../InputData3.xlsx')
    data = pd.read_excel(filePath, encoding='gbk')
    dict_temp = {'T-North':0,'T-Center':1,'T-South':2,'S-North':3,'S-Center':4,'S-South':5,'S-East':6}
    res = data[strb][dict_temp[stra]]
    time = int(res)
    return time

#计算时间a和时间b的时间间隔，以分表示
def calcTime(stra,strb):
    t1 = int(stra[:2]) * 60 + int(stra[2:])
    t2 = int(strb[:2]) * 60 + int(strb[2:])
    return abs(t1 - t2)

#计算换乘紧张度
def calcTransferTension(a,b,arr,leave,gatea,gateb):
    '''
    :param a: 出发时间,str,如：1700
    :param b: 到达时间，str，如：0000
    :param arr: 到达，字典{0:'DT',1:'DS',2:'IT',3:'IS'}的key
    :param leave: 出发，字典{0:'DT',1:'DS',2:'IT',3:'IS'}的key
    :param gatea: 登机口a，{0:'T-North',1:'T-Center',2:'T-South',3:'S-North',4:'S-Center',5:'S-South',6:'S-East'}
    :param gate: 登机口b，{0:'T-North',1:'T-Center',2:'T-South',3:'S-North',4:'S-Center',5:'S-South',6:'S-East'}
    :return: 换乘紧张度
    '''
    linktime = calcTime(a,b) - 45
    route, cnt  =passengerFlow(arr,leave)
    waltime = walkTime(gatea,gateb)
    excTime = route+cnt*8+waltime
    JZD = excTime/linktime
    return JZD,linktime

def distributeOfExcTime(excTimeList):
    totalDic = {}
    m = int((max(excTimeList)/10))*10+5
    for i in range(5,m,5):
        #iList.append(i)
        subs = str(i)
        dics = {subs:0}
        totalDic.update(dics)
        dics.clear()
    for times in excTimeList:
        for keys in totalDic:
            if int(times)<= int(keys):
                totalDic[keys] +=1
    return sorted(totalDic.items(),key=lambda item:item[1])

def distributeOfJZD(JZDlist):
    m = int(max(JZDlist)*10)
    totalDic = {}
    for i in range(1,m):
        subs = str(float(i)/10.)
        dics = {subs:0}
        totalDic.update(dics)
        dics.clear()
    for jzd in JZDlist:
        for keys in totalDic:
            if float(jzd)<= float(keys):
                totalDic[keys] +=1
    return sorted(totalDic.items(),key=lambda item:item[1])

def drawPictime(list):
    dict = distributeOfExcTime(list)
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    xlist = []
    ylist = []
    for keys in dict:
        xlist.append(int(keys[0]))
        ylist.append(int(keys[-1]))
    maxNum = max(ylist)
    for index,num in enumerate(ylist):
        ylist[index]=float(float(num)/float(maxNum))
    plt.plot(xlist, ylist)
    plt.bar(xlist, ylist,color='rgb', tick_label=xlist)
    # for a, b in zip(xlist, ylist):
    #     plt.text(a, b + 0.05, '%.2f' % b, ha='center', va='bottom', fontsize=11)
    plt.xticks(xlist[::50], xlist[::50], rotation=0)
    plt.xlabel(u'换乘时间（分钟）')
    plt.ylabel(u'比率')
    plt.title(u'总体旅客换乘时间分布图')
    plt.savefig(u'总体旅客换乘时间分布图.jpg')
    plt.show()

def drawPicjzd(list):
    colors = ['red', 'blue', 'green', 'orange', 'black']
    dict = distributeOfJZD(list)
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    xlist = []
    ylist = []
    for keys in dict:
        xlist.append(str(keys[0]))
        ylist.append(float(keys[-1]))
    maxNum = max(ylist)
    for index,num in enumerate(ylist):
        ylist[index]=float(float(num)/float(maxNum))
        if int(num) == 1:
            break
    xlist = xlist[:50]
    ylist = ylist[:50]
    plt.plot(xlist, ylist,c='black')
    plt.bar(xlist, ylist,color='rgb', tick_label=xlist)
    plt.xticks(xlist[::10], xlist[::10], rotation=30)
    plt.xlabel(u'紧张度')
    plt.ylabel(u'比率')
    plt.title(u'总体旅客换乘紧张度分布图')
    plt.savefig(u'总体旅客换乘紧张度分布图.jpg')
    plt.show()

def read_dict(file_dir):
    # 读取结果
    with open(file_dir, 'r') as f:
        a = f.read()
        dic_name = eval(a)
        f.close()
    return dic_name

# 保存最终结果到excel文件中
def saveresults():
    res1 = read_dict('../solution/problem1/result.txt')
    res2 = read_dict('../solution/problem2/result.txt')
    res3 = read_dict('../solution/problem3/result.txt')

    old_excel = xlrd.open_workbook('../InputData.xlsx')
    new_excel = copy(old_excel)
    ws = new_excel.get_sheet(0) # Pucks

    # for i in range(1,753):
    #     for j in range(12,14):
    #         ws.write()

    for rkey, rval in res1.items():
        for r in rval:
            ws.write(int(r.replace('PK','')),12,rkey)

    for rkey, rval in res2.items():
        for r in rval:
            ws.write(int(r.replace('PK','')),13,rkey)

    for rkey, rval in res3.items():
        for r in rval:
            ws.write(int(r.replace('PK','')),14,rkey)

    new_excel.save('../result.xls')

if __name__ == '__main__':
    # 保存三个问题的分配结果
    saveresults()