from lib.dataloader import read_data,data_filter
import networkx as nx

if __name__ == '__main__':
    P, T, G = read_data('../../')
    Pucks = data_filter(P)
    G = nx.Graph()
    G.add_nodes_from([p for p in Pucks.keys()])

    for p in Pucks.keys():
        for q in Pucks.keys():
            if p == q:
                continue
