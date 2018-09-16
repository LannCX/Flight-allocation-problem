import pandas as pd
from lib import dataloader

# 统计每个航班的人数（带星号航班不考虑）
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

# 旅客流程
def passengerFlow(a,b):
    '''
    数字a为表格InputData2.xlsx的列索引，数字b为其行索引
    :param a:表格索引{0:'DT',1:'DS',2:'IT',3:'IS'}
    :param b:表格索引{0:'DT',1:'DS',2:'IT',3:'IS'}
    :return:route：最短流程时间，cnt：捷运乘坐次数
    '''
    filePath = (r'InputData2.xlsx')
    data = pd.read_excel(filePath, encoding='gbk')
    dict_temp = {0: 'DT', 1: 'DS', 2: 'IT', 3: 'IS'}
    res = data[dict_temp[a]][b]
    route = int(res[:2])
    cnt = int(res[-1])
    return route,cnt

#旅客行走时间，从登机口区域a走到b
def walkTime(a,b):
    '''
    :param a:表格索引{0:'T-North',1:'T-Center',2:'T-South',3:'S-North',4:'S-Center',5:'S-South',6:'S-East'}
    :param b:表格索引{0:'T-North',1:'T-Center',2:'T-South',3:'S-North',4:'S-Center',5:'S-South',6:'S-East'}
    :return:从登机口区域a走到b的时间
    '''
    filePath = (r'InputData3.xlsx')
    data = pd.read_excel(filePath, encoding='gbk')
    dict_temp = {0:'T-North',1:'T-Center',2:'T-South',3:'S-North',4:'S-Center',5:'S-South',6:'S-East'}
    res = data[dict_temp[a]][b]
    time = int(res)
    return time

#获取时间字符串的时分秒
def getTime(str):
    hrs = int(str[:2])
    mins = int(str[-2:])
    secs = 00
    return hrs,mins,secs

#计算时间a和时间b的时间间隔，以分表示
def calcTime(stra,strb):
    import datetime
    ahrs,amins,asecs = getTime(stra)
    bhrs,bmins,bsecs = getTime(strb)
    a = str(ahrs)+':'+str(amins)+':'+str(asecs)
    b = str(bhrs)+':'+str(bmins)+':'+str(bsecs)
    timea = datetime.datetime.strptime(a,"%H:%M:%S")
    timeb = datetime.datetime.strptime(b,"%H:%M:%S")
    if timea < timeb:
        link = (timeb - timea)
    else:
        link = (timea - timeb)
    linkTime = list(str(link))
    h = linkTime[0]+linkTime[1]
    min = linkTime[3]+linkTime[4]
    return int(h)*60+int(min)

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
    linktime = calcTime(a,b)
    route,count =passengerFlow(arr,leave)
    waltime = walkTime(gatea,gateb)
    excTime = route+count*8+waltime
    JZD = excTime/linktime
    return JZD

# 计算最短流程时间
def calc_min_flow(puck,gate):

    pass

if __name__ == '__main__':
    pass