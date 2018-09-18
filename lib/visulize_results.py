import numpy as np
import matplotlib as plt
from lib.dataloader import aircraft
from lib.utils import calcTime

# 成功分配到登机口的航班数量，按照宽窄机型分别画出现状图
def puckto_gates(file_path,pucks):
    n_W = 0
    n_N = 0
    all_W = 0
    all_N = 0
    # 读取结果
    with open(file_path, 'r') as f:
        a = f.read()
        res = eval(a)
        f.close()
    for pval in pucks.values():
        if pval['飞机型号'] in aircraft['W']:
            all_W += 1
        else:
            all_N += 1

    for rkey, rval in res.items():
        for p in rval:
            if pucks[p]['飞机型号'] in aircraft['W']:
                n_W += 1
            else:
                n_N += 1

    return all_W,all_N,n_W,n_N

# T和S登机口的使用数目和被使用登机口的平均使用率（登机口占用时间比率），要求画线状图
def useRate(file_path,pucks,gates):
    # 读取结果
    with open(file_path, 'r') as f:
        a = f.read()
        res = eval(a)
        f.close()

    # T和S登机口数目
    n_T = 0
    n_S = 0
    rate_T = []
    rate_S = []
    print(len(res))
    for rkey, rval in res.items():
        # n = len(rval)
        dt = 0
        if gates[rkey]['终端厅'] == 'T':
            n_T += 1
            # T平均使用率
            for r in rval:
                dt += calcTime(pucks[r]['到达时刻'],pucks[r]['出发时刻']) - 45
            rate_T.append(dt / (24 * 60))
        else:
            n_S += 1
            # S平均使用率
            for r in rval:
                dt += calcTime(pucks[r]['到达时刻'], pucks[r]['出发时刻']) - 45
            rate_S .append(dt / (24 * 60))

    return n_T,n_S,sum(rate_T)/len(rate_T),sum(rate_S)/len(rate_S)

# TODO: 仅限问题二、三：总体旅客换乘时间分布图
def transfer_time():
    pass

# TODO: 仅限问题二、三：总体旅客换乘紧张度分布图
def tensity_distr():
    pass


