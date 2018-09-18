from lib.visulize_results import puckto_gates
from lib.dataloader import read_data,data_filter

if __name__ == '__main__':
    P, T, G = read_data('../../')
    Pucks = data_filter(P)
    print(puckto_gates('result.txt',Pucks))

    pass