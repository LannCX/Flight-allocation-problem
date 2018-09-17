import numpy as np
import matplotlib as np

# TODO:成功分配到登机口的航班数量，按照宽窄机型分别画出现状图
def plot_puckto_gates():
    # 读取结果
    with open('solution/problem1/result.txt', 'r') as f:
        a = f.read()
        dict_name = eval(a)
        f.close()

# TODO: T和S登机口的使用数目和被使用登机口的平均使用率（登机口占用时间比率），要求画线状图
def useRate():
    pass

# TODO: 仅限问题二、三：给出换乘失败旅客数量和比率
def fail_transfer():
    pass

# TODO: 仅限问题二、三：总体旅客换乘时间分布图
def transfer_time():
    pass

# TODO: 仅限问题二、三：总体旅客换乘紧张度分布图
def tensity_distr():
    pass
