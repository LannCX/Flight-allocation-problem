from lib.visulize_results import puckto_gates,useRate
from lib.dataloader import read_data,data_filter

if __name__ == '__main__':
    P, T, G = read_data('../../')
    Pucks = data_filter(P)
    file_name = 'result.txt'
    print(puckto_gates(file_name,Pucks))
    print(useRate(file_name,Pucks,G))
    pass