from lib.visulize_results import puckto_gates,useRate
from lib.dataloader import read_data,data_filter
from lib.utils import drawPictime,drawPicjzd

if __name__ == '__main__':
    P, T, G = read_data('../../')
    Pucks = data_filter(P)
    file_name = 'result.txt'
    print(puckto_gates(file_name,Pucks))
    print(useRate(file_name,Pucks,G))

    with open('opt_flow.txt', 'r') as f:
        a = f.read()
        opt_flow = eval(a)
        f.close()

    drawPictime(opt_flow)

    with open('opt_tens.txt', 'r') as f:
        a = f.read()
        opt_tens = eval(a)
        f.close()

    drawPicjzd(opt_tens)