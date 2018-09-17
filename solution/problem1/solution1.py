from lib.dataloader import read_data,data_filter
from lib import algorithm
import matplotlib.pyplot as plt

# 蒙特卡洛搜索
N = 1000
maxscore = 0
for i in range(N):
    P, T, G = read_data('../../')
    Pucks = data_filter(P)
    DG = algorithm.createG(Pucks)

    # 求解最优匹配
    Gmap = algorithm.matchG(DG, G, P)

    # 计算目标函数值
    score = algorithm.calcObj(Gmap,1)
    # TODO:不同的问题可能是最小化
    if score > maxscore:
        maxscore = score
    plt.scatter(i,maxscore,c='b')
    print('Iteration %d: score=%d, num of gates: %d'%(i+1,maxscore,len(Gmap)))
plt.xlabel('iter')
plt.ylabel('Score')
plt.show()