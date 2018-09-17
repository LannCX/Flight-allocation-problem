from lib.dataloader import aircraft
from lib.utils import calcTime
import random
import networkx as nx

# 创建图，并根据宽窄机型和时间差添加边
def createG(pucks):
    DG = nx.DiGraph()
    DG.add_nodes_from([p for p in pucks.keys()])
    for p in pucks.keys():
        for q in pucks.keys():
            if p == q:
                continue
            a = pucks[p]['飞机型号'] in aircraft['W']
            b = pucks[q]['飞机型号'] in aircraft['W']
            if ((a and b) or (not a and not b)) and pucks[p]['出发时刻'] <= pucks[q]['到达时刻']:
                DG.add_edge(p,q)

    return DG

# 按照规则给图添加权重/概率
def init_weight(dg,gates,pucks,lamda=10):
    # 统计每种不同出入类别的数量
    Gn = {}
    for gkey, gval in gates.items():
        s = gval['到达类型'] + ':' + gval['出发类型']
        if s not in Gn.keys():
            Gn[s] = 1
        else:
            Gn[s] += 1
    # 检查一下
    # if sum([val for val in Gn.values()]) != 69:
    #     raise ('出入类型数据统计错误！！！')

    # 遍历边, 计算权重/概率
    for node in dg.nodes(data=False):
        sumlist = {}
        s_all = 0

        for neib in dg.neighbors(node):
            dt = lamda * calcTime(pucks[neib]['出发时刻'],pucks[node]['出发时刻'])
            s_neib = 0
            for gn in Gn.keys():
                if pucks[neib]['到达类型'] in gn.split(':')[0] and pucks[node]['到达类型'] in gn.split(':')[0] \
                        and pucks[neib]['出发类型'] in gn.split(':')[1] and pucks[node]['出发类型'] in gn.split(':')[1]:
                    ita = 1
                else:
                    ita = 0
                s_neib += ita * Gn[gn]
            if s_neib == 0:
                res = 0
            else:
                res = dt + s_neib
            s_all += res
            sumlist[node+':'+neib] = res

        for skey, sval in sumlist.items():
            if sval == 0:
                dg.remove_edge(skey.split(':')[0],skey.split(':')[-1])
            else:
                dg[skey.split(':')[0]][skey.split(':')[-1]]['weight'] = sval/s_all

    return dg

# 寻找最长路径
def findroute(dG):
    route_dic = {}
    opt_rt = []

    # 找到初始点
    start_nodes = [a for a in dG.nodes if dG.in_degree(a) == 0]
    end_nodes = [b for b in dG.nodes if dG.out_degree(b) == 0]
    count = 0
    for p in start_nodes:
        node = p
        route = [p]
        is_continue = True
        while (node not in end_nodes) and is_continue:
            # 每次迭代产生一个新的路径节点
            rn = random.random()
            s = 0
            for neib in dG.neighbors(node):
                if neib == None:
                    break
                if rn > s and rn <= s + dG[node][neib]['weight']:
                    node = neib
                    route.append(neib)
                    is_continue = True
                    break
                else:
                    s += dG[node][neib]['weight']
                    is_continue = False

        route_dic[count] = route
        count +=1

    # 选择最长的路径
    for rt in route_dic.values():
        if len(rt) > len(opt_rt):
            opt_rt = rt

    return opt_rt

# 匹配航班和登机口
def matchG(dg, Gates, pucks):
    gates = Gates
    Gmap = {}
    match_flag = True
    while match_flag:
        dg = init_weight(dg,gates,pucks)
        longest_rt = findroute(dg)
        if gates.keys() == None or len(longest_rt)<=1:
            break
        # 判断还能否分配登机口
        for gkey, gval in gates.items():
            for pk in longest_rt:
                if pucks[pk]['到达类型'] not in gval['到达类型'] or pucks[pk]['出发类型'] not in gval['出发类型']:
                    match_flag = False
                    break
                else:
                    match_flag = True

            # 全部航班匹配该登机口
            if match_flag:
                matched_key = gkey
                Gmap[gkey] = longest_rt
                break

        if match_flag:
            dg.remove_nodes_from(longest_rt) # 删除已匹配节点
            gates.pop(matched_key) # 删除已匹配登机口
    return Gmap

# TODO: 计算目标函数(问题2,3)
def calcObj(Gmap,prob_num=1):
    score = 0
    if prob_num == 1:
        score = sum([len(val) for val in Gmap.values()])
    elif prob_num == 2:
        score = None
    elif prob_num == 3:
        score = None
    else:
        raise ('Invalid prob_num, it should in {1,2,3}')
    return score