from lib.dataloader import aircraft, read_data,data_filter,tickets_filter
from lib.utils import calcTime,passengerFlow,calcTransferTension
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
def init_weight(dg,gates,pucks,tickets,lamda=10):
    # 统计每种不同出入类别的数量
    Gn = {}
    for gkey, gval in gates.items():
        s = gval['到达类型'] + ':' + gval['出发类型']
        if s not in Gn.keys():
            Gn[s] = 1
        else:
            Gn[s] += 1

    # 遍历节点，添加属性
    # for node in dg.nodes(data=False):
    #     success = 0
    #     for tkey, tval in tickets.items():
    #         arrive_flight = None
    #         leave_flight = None
    #         if tval['到达航班'] == pucks[node]['到达航班']:
    #             arrive_flight = pucks[node]['到达类型']
    #         if tval['出发航班'] == pucks[node]['出发航班']:
    #             leave_flight = pucks[node]['出发类型']
    #
    #         # 当到达和出发航班都找到了登机口的时候换乘成功
    #         if arrive_flight != None and leave_flight != None:
    #             success += tval['乘客数']
    #     dg.node[node]['weight'] = success

    # 遍历边, 计算权重/概率
    for node in dg.nodes(data=False):
        sumlist = {}
        s_all = 0
        for neib in dg.neighbors(node):
            dt = lamda * calcTime(pucks[neib]['出发时刻'],pucks[node]['出发时刻'])
            # n_tickets = dg.node[node]['weight'] + dg.node[neib]['weight']
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

def matchG(dg, Gates, pucks, tickets):
    gates = Gates
    Gmap = {}
    match_flag = True
    while match_flag:
        dg = init_weight(dg,gates,pucks,tickets)
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

# 问题三的目标函数
def calcTotalTensity(map):
    failed = 0
    total_people = 0
    tensity = []
    P, T, G = read_data('../../')
    Pucks = data_filter(P)
    Tickets = tickets_filter(T)
    flow = []

    # count = 0
    # for tkey, tval in Tickets.items():
    #     total_people += tval['乘客数']
    #     arrive_flight = None
    #     leave_flight = None
    #     for pkey, pval in Pucks.items():
    #         if tval['到达航班'] == pval['到达航班']:
    #             arrive_flight = pval['到达类型']
    #         if tval['出发航班'] == pval['出发航班']:
    #             leave_flight = pval['出发类型']
    #
    #     # 当到达和出发航班都找到了登机口的时候换乘成功
    #     if arrive_flight != None and leave_flight != None:
    #         success += tval['乘客数']
    #     # 换乘失败：没有匹配完整的到达和出发航班
    #     else:
    #         failed += tval['乘客数']

    # 每张票找最短流程
    for tkey, tval in Tickets.items():
        total_people += tval['乘客数']
        arrive_flight = None
        leave_flight = None
        for mkey, mval in map.items():
            for pk in mval:
                if tval['到达航班'] == Pucks[pk]['到达航班']:
                    arrive_flight = Pucks[pk]['到达类型'] + G[mkey]['终端厅']
                    arrive_time = Pucks[pk]['到达时刻']
                    arrive_area = G[mkey]['终端厅'] + '-' + G[mkey]['区域']
                if tval['出发航班'] == Pucks[pk]['出发航班']:
                    leave_flight = Pucks[pk]['出发类型'] + G[mkey]['终端厅']
                    leave_time = Pucks[pk]['出发时刻']
                    leave_area = G[mkey]['终端厅'] + '-' + G[mkey]['区域']

        # 当到达和出发航班都找到了登机口的时候换乘成功
        if arrive_flight != None and leave_flight != None:
            ts, trans_time = calcTransferTension(arrive_time,leave_time,arrive_flight,leave_flight,arrive_area,leave_area)
            for i in range(int(tval['乘客数'])):
                flow.append(trans_time)
                tensity.append(ts)
        # 换乘失败：没有匹配完整的到达和出发航班
        else:
            failed += tval['乘客数']

    return tensity,flow,int(failed),int(total_people),

if __name__ == '__main__':
    # 蒙特卡洛搜索
    N = 100
    optscore = 0
    opt_gmap = {}
    score_list = []
    optscore_list = []
    gates_list = []
    optgates_list = []

    for i in range(N):
        P, T, G = read_data('../../')
        Pucks = data_filter(P)
        Tickets = tickets_filter(T)
        DG = createG(Pucks)

        # 求解最优匹配
        Gmap = matchG(DG, G, Pucks, Tickets)

        # 计算目标函数值
        score = sum([len(x) for x in Gmap.values()])
        tens,Flow,n_fail,n_all = calcTotalTensity(Gmap)

        # 航班分配最多
        if score > optscore:
            optscore = score
            opt_gmap = Gmap
            opt_n_fail = n_fail
            opt_n_all = n_all
            opt_tens = tens
            opt_flow = Flow
            with open('result.txt','w') as f:
                f.write(str(opt_gmap))
                f.close()
        # 最小化紧张度
        elif score == optscore and sum(tens) < sum(opt_tens):
            optscore = score
            opt_gmap = Gmap
            opt_n_fail = n_fail
            opt_n_all = n_all
            opt_tens = tens
            opt_flow = Flow
            with open('result.txt', 'w') as f:
                f.write(str(opt_gmap))
                f.close()

        optscore_list.append(optscore)
        optgates_list.append(len(opt_gmap))

        print('Iteration %d: score:%d, total tensity:%f, optscore:%d, opt_gate:%d, num of tensity: %f'%(i+1,score,sum(tens),optscore,len(opt_gmap),sum(opt_tens)))

    # 打印并保存结果
    print('换乘失败人数: %d, 总人数:%d, 换乘失败比率: %f'%(opt_n_fail,opt_n_all,opt_n_fail/opt_n_all))
    with open('opt_flow.txt','w') as f:
        f.write(str(opt_flow))
    with open('optscore_list.txt','w') as f:
        f.write(str(optscore_list))
    with open('opt_tens.txt','w') as f:
        f.write(str(opt_tens))
    with open('optgates_list.txt','w') as f:
        f.write(str(optgates_list))