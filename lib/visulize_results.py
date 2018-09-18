import numpy as np
import matplotlib as plt
from lib.dataloader import aircraft

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

# TODO: T和S登机口的使用数目和被使用登机口的平均使用率（登机口占用时间比率），要求画线状图
def useRate(pucks):
    pass

# TODO: 仅限问题二、三：总体旅客换乘时间分布图
def transfer_time():
    pass

# TODO: 仅限问题二、三：总体旅客换乘紧张度分布图
def tensity_distr():
    pass


