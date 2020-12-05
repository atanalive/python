import numpy as np
import copy
import matplotlib.pyplot as plt
import time
import pandas as pd

city_num = 10  # 城市的个数
population_size = 100  # 种群
selfadj = False  # 为真时是自适应
iter_max = 10 ** 3  # 最大循环次数
pc = 0.85  # 交叉概率
pw = 0.15  # 变异概率
# 城市坐标
# 10city
# city_loc = np.array([[54, 19, 20, 12, 88, 74, 55, 1, 78, 21], [55, 70, 18, 63, 59, 92, 23, 73, 16, 28]])
# 20city
# city_loc = np.array([[75, 14, 78, 31, 88, 34, 1, 32, 69, 10, 91, 12, 41, 88, 59, 89, 44, 20, 99, 33]
#                         , [64, 26, 35, 69, 38, 66, 83, 72, 37, 34, 24, 0, 88, 83, 85, 22, 61, 66, 65, 15]])
# 100city
city_loc = np.array([[75,16,38,52,41,61,34,14,0,74,51,6,87,77,93,35,59,20,11,32,96,57,83,75,15,42,75,3,2,4,55,1,53,54,72,55,36,75,58,19,86,86,63,79,92,65,13,0,10,72,14,89,0,27,98,85,20,99,44,42,3,35,67,12,92,26,2,85,31,73,63,64,86,62,98,57,2,36,81,81,8,33,10,24,68,31,84,67,54,89,30,44,21,69,17,18,47,4,80,59]
                         , [5,82,1,35,35,38,93,9,29,71,19,11,29,93,42,39,62,89,79,96,92,67,40,58,91,86,28,76,57,81,46,90,64,55,87,20,52,93,65,17,80,51,34,81,46,6,7,46,86,68,38,63,50,98,68,28,90,20,67,96,20,91,78,15,58,62,90,52,68,52,72,37,13,54,42,83,86,6,19,87,6,84,29,59,57,20,38,68,72,60,65,12,25,6,84,5,42,81,5,22]])

city_size = len(city_loc[0, :])
city_distance_matrix = np.zeros((city_size, city_size))  # 城市距离矩阵
population = []  # 种群
unit_distance = [None] * population_size  # 初始化个体的距离列表
unit_fitness = [None] * population_size  # 初始化个体的适应度


# 城市距离矩阵
def calculate_city_distance():
    for i in range(city_size):
        for j in range(city_size):
            city_distance_matrix[i, j] = np.sqrt(np.sum(np.power(city_loc[:, i] - city_loc[:, j], 2)))


# 初始化种群
def init_population():
    for i in range(population_size):
        population.append(new_unit())


def new_unit():
    unit = np.arange(city_size - 1) + 1
    np.random.shuffle(unit)  # 打乱种群 自动赋值
    unit = np.insert(unit, 0, 0)  # 不会自动赋值，要手动赋值 （目标，位置，插入值）
    return unit


# 计算每个染色体的路径长度
def calculate_unit_distance():
    for idx, n in enumerate(population):
        distance = 0
        for i in range(city_size - 1):
            distance += city_distance_matrix[n[i], n[i + 1]]
        distance += city_distance_matrix[n[i + 1], n[0]]
        unit_distance[idx] = distance


# 计算每个染色体的适应度
def calculate_fitness():
    for idx, n in enumerate(unit_distance):
        unit_fitness[idx] = 1 / n


# 找到最好的染色体
def find_the_best():
    best_idx = -1
    best_fitness = best_unit_fitness
    for idx, n in enumerate(unit_fitness):
        if best_fitness < n:
            best_fitness = n
            best_idx = idx
    if best_idx == -1:
        return best_unit, best_fitness
    return population[best_idx], best_fitness


# 开始选择下一代
def choose_new_position():
    old_population = population[:]
    # 求得适应度sum数组，便于抽样
    unit_fitness_sum = [None] * population_size
    for idx, n in enumerate(unit_fitness):
        if idx == 0:
            unit_fitness_sum[idx] = unit_fitness[idx]
        else:
            unit_fitness_sum[idx] = unit_fitness[idx] + unit_fitness_sum[idx - 1]

    # 根据适应度抽取原先大小种群为下一代
    for i in range(population_size):
        sample = np.random.uniform(0, unit_fitness_sum[population_size - 1])
        for j in range(population_size):
            if j == 0 and sample < unit_fitness_sum[j]:
                break
            elif unit_fitness_sum[j - 1] < sample and unit_fitness_sum[j] > sample:
                break
        population[i] = old_population[j]


# 交叉产生新染色体，交叉互换
def cross_population():
    global pc
    if selfadj == True:  # 随着迭代的进行，进行退火处理
        pc = pc * 0.9
    for i in range(population_size):
        p_sample = np.random.uniform(0, 1)
        if p_sample > pc:
            # random.randint为【】，np.random.randint为【)
            dst_unit = np.random.randint(population_size)
            gene_cross(i, dst_unit)


# 基因交换
def gene_cross(idx1, idx2):
    # 随机抽取索引
    cross_idx1, cross_idx2 = np.random.choice(np.arange(city_size), 2)
    if cross_idx1 > cross_idx2:
        cross_idx1, cross_idx2 = cross_idx2, cross_idx1
    # 交换片段
    # 如果不copy的话，numpy元素无法顺利交换
    # 在对面染色体对应段找到自己染色体对应元素所在位置进行交换
    for i in range(cross_idx1, cross_idx2 + 1):
        value1 = population[idx2][i]
        value2 = population[idx1][i]
        index1 = np.squeeze(np.where(population[idx1] == value1))
        index2 = np.squeeze(np.where(population[idx2] == value2))
        population[idx1][index1], population[idx1][i] = population[idx1][i], population[idx1][index1]
        population[idx2][index2], population[idx2][i] = population[idx2][i], population[idx2][index2]


# 基因突变
def gene_mutation():
    global pw
    if selfadj == True:  # 随着迭代的进行，进行退火处理
        pc = copy.deepcopy(pw * 0.9)
    for i in range(population_size):
        p_sample = np.random.uniform(0, 1)
        if p_sample > pw:
            population[i] = new_unit()


def draw():
    point = city_loc[:, best_unit]
    point = np.insert(point, point[0].size, city_loc[:, 0], axis=1)
    plt.style.use("ggplot")
    plt.plot(point[0], point[1], color="#1E90FF")
    plt.title("made by Alive")
    plt.show()
    run_time = round(time.time() - time_start, 2)
    shortest_distance = round(1 / best_unit_fitness, 2)
    print(f'''
    shortest distance is {shortest_distance}
    best_unit_fitness is {best_unit_fitness:2f}
    run time is {run_time}
    path is 
    {best_unit}
    ''')


best_unit = None
best_unit_fitness = 0
time_start = None
if __name__ == "__main__":
    time_start = time.time()
    # 计算城市距离矩阵
    calculate_city_distance()

    # 初始化种群
    init_population()

    iter = 0
    for i in range(iter_max):
        # 计算每个染色体的路径长度
        calculate_unit_distance()

        # 计算每个染色体的适应度
        calculate_fitness()

        # 找到适应度最高的染色体
        best_unit, best_unit_fitness = find_the_best()

        # 根据适应度选择下一代
        choose_new_position()

        # 交叉互换
        cross_population()

        # 基因突变
        gene_mutation()

    # 迭代结束，画出最优路径
    draw()
