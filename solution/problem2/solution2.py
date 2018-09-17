from lib.dataloader import read_data,data_filter,aircraft
from lib.utils import calcTime,calcObj
import random
import networkx as nx
import matplotlib.pyplot as plt

# 创建图，并根据宽窄机型和时间差添加边
def createG(pucks):
    DG = nx.DiGraph()
    DG.add_nodes_from([p for p in Pucks.keys()])
    for p in pucks.keys():
        for q in pucks.keys():
            if p == q:
                continue
            a = pucks[p]['飞机型号'] in aircraft['W']
            b = pucks[q]['飞机型号'] in aircraft['W']
            if ((a and b) or (not a and not b)) and pucks[p]['出发时刻'] <= pucks[q]['到达时刻']:
                DG.add_edge(p,q)

    return DG

# TODO: 按照规则给图添加权重
def calc_weight(DG,Gates,Pucks):
    # 统计每种不同出入类别的数量
    Gn = {}
    for gkey, gval in Gates.items():
        s = gval['到达类型'] + ':' + gval['出发类型']
        if s not in Gn.keys():
            Gn[s] = 1
        else:
            Gn[s] += 1
    # 检查一下
    if sum([val for val in Gn.values()]) != 69:
        raise ('出入类型数据统计错误！！！')

    # 遍历边
    for u, v in DG.edges(data=False):
        # 计算权重/概率
        Pucks[u]['']


    return DG

# TODO: 寻找最长路径
def findroute(DG,puck):
    route_list = []
    for x in DG.neighbors(puck):
        pass

    while True:
        pass

    return route_list

# TODO: 匹配航班和登机口
def matchG(DG, Gates):
    Gmap = {}
    # 找到初始点
    start_nodes = [a for a in DG.nodes if DG.in_degree(a) == 0]
    # end_nodes = [b for b in DG.nodes if DG.out_degree(b) == 0]
    maxl = 0
    opt_rt = []
    for p in start_nodes:
        rt = findroute(DG, p)
        if len(rt) > maxl:
            maxl = len(rt)
            opt_rt = rt

    # if suc:
    #     DG.remove_nodes_from(rt)
    #     Gates.pop(optG)
    return Gmap


# 马尔科夫蒙特卡洛算法
def mcmc(Pucks, Gates, N):
    DG = createG(Pucks)
    maxscore = 0
    for i in range(N):
        Gmap = matchG(DG,Gates)
        score = calcObj(Gmap)
        if score > maxscore:
            maxscore = score
        plt.plot(i,maxscore)
        print('Iteration %d: score=%d'%(i,maxscore))
    plt.xlabel('iter')
    plt.ylabel('Score')
    plt.show()

    return maxscore,Gmap

if __name__ == '__main__':
    P, T, G = read_data('../../')
    Pucks = data_filter(P)
    mcmc(Pucks,G,10000)