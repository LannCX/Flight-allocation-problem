from lib.dataloader import read_data,data_filter,aircraft
import networkx as nx

if __name__ == '__main__':
    P, T, G = read_data('../../')
    Pucks = data_filter(P)
    DG = nx.DiGraph()
    DG.add_nodes_from([p for p in Pucks.keys()])

    for p in Pucks.keys():
        for q in Pucks.keys():
            if p == q:
                continue
            a = Pucks[p]['飞机型号'] in aircraft['W']
            b = Pucks[q]['飞机型号'] in aircraft['W']
            if ((a and b) or (not a and not b)) and Pucks[p]['出发时刻'] <= Pucks[q]['到达时刻'] and Pucks[q]['到达日期'] != '2018-01-19':
                DG.add_edge(p,q)

    print(len(list(DG.adj['PK267'])))