import numpy as np
import random
from cost import Mathod
import time

size = 3  # 大小
# 头结点
head = np.array([4, 1, 5, 3, 8, 7, 6, 0, 2]).reshape(size, size)
# 目标节点
state_dst = np.arange(0, size * size).reshape((size, size))


# 八数码的有解无解问题：除以0以外的逆数对的个数的奇偶性相同则有解，否则无解
def check_if_sulotion():
    # 如果两个逆数对的奇偶性不同则无解
    if reverse_pair(head) % 2 != reverse_pair(state_dst) % 2:
        exit('''
        program end!
        it has no sulotion''')


# 求逆数对 即每个数字与前面比它大的数字组成的数字对
def reverse_pair(num):
    num = num.reshape(num.shape[0] * num.shape[1])
    count = 0
    for i in range(1, len(num)):
        # range(0)时不会进入下面执行
        for j in range(i):
            if num[i] == 0:
                break
            if num[j] > num[i]:
                count += 1
    return count


def check_if_exit():
    # 如果超过了最大次数则退出
    if iter >= max_iter:
        print('''
               program end
               max_iter {}
               run time is {:.2f}
               please modify the program for better'''.format(max_iter, 0))
        exit("you over the max_iter")


def check_openList_if_null():
    # 如果open表为空则退出
    if len(openList) == 0:
        exit('''
               program end
               openList is empty''')


def check_if_finish():
    import time
    time_end = time.time()
    time = time_end - time_start
    if (state_now == state_dst).all():
        print("\r", end=" ")  # 清除以前的输出
        print(f'''
        mathod is {mathod.mathod}
        iter is {iter} times
        the begin state is
        {head[0]}
        {head[1]}
        {head[2]}
        the last state is
        {state_now[0]}
        {state_now[1]}
        {state_now[2]}
        successful!!!
        run time is {time:.3f}s''')
        exit()


def expand_and_get_openList():
    # 拓展openList
    add_openList = expand_openList()
    # 去除openList里面与closeList重复的部分
    remove_duplicates(add_openList)
    # 添加新获得的节点
    add_new_openlist(add_openList)
    # 检查openlist是否为空
    check_openList_if_null()
    # 取得下一个state
    next_state = get_next_state()
    return next_state


def expand_openList():
    # 得到0的位置
    # 法1
    x, y = find_zero_instate_index()
    add_openList = []
    # 法2
    # x, y = np.argwhere(state_now == 0)
    if y > 0:
        state_tmp = zero_moving(x, y, "left")
        add_g(state_tmp)
        add_openList.append(state_tmp)
    if y < size - 1:
        state_tmp = zero_moving(x, y, "right")
        add_g(state_tmp)
        add_openList.append(state_tmp)
    if x > 0:
        state_tmp = zero_moving(x, y, "up")
        add_g(state_tmp)
        add_openList.append(state_tmp)
    if x < size - 1:
        state_tmp = zero_moving(x, y, "down")
        add_g(state_tmp)
        add_openList.append(state_tmp)
    return add_openList.copy()


def add_g(state):
    if g.get(np.array2string(state)) == None:
        g[np.array2string(state)] = g[np.array2string(state_now)] + g_plus
        return
    g[np.array2string(state)] = np.min([g[np.array2string(state)], g[np.array2string(state_now)] + g_plus])


def zero_moving(x, y, direction):
    # 这里一定要copy，不然numpy传的是引用，会出大问题
    state_next = state_now.copy()
    if direction == "up":
        state_next[x, y] = state_next[x - 1, y]
        state_next[x - 1, y] = 0
    elif direction == "down":
        state_next[x, y] = state_next[x + 1, y]
        state_next[x + 1, y] = 0
    elif direction == "left":
        state_next[x, y] = state_next[x, y - 1]
        state_next[x, y - 1] = 0
    elif direction == "right":
        state_next[x, y] = state_next[x, y + 1]
        state_next[x, y + 1] = 0
    return state_next


def find_zero_instate_index():
    # 查找0所在位置
    for i, list in enumerate(state_now):
        for j, value in enumerate(list):
            if value == 0:
                return i, j


def remove_duplicates(add_openList):
    # 在迭代器内部删除元素要注意的事项：1，在自身迭代中删除元素，没删除一次会跳过一个索引 2. 要用副本进行迭代
    # 去除openlist里与closelist重复的部分
    count = 0
    for i, n in enumerate(add_openList[:]):
        for m in closeList:
            if (n == m).all():
                # 当前状态的g不能删，计算cost的时候还要用
                if (n != state_now).all() and g.get(np.array2string(n)) != None:
                    del g[np.array2string(n)]
                del add_openList[i - count]
                count += 1


def add_new_openlist(add_openList):
    # 添加新获得的openlist
    for n in add_openList:
        openList.append(n)


# 取得下一个state
def get_next_state():
    min_cost = mathod.cost(openList[0], state_dst) + g[np.array2string(openList[0])]
    min_idx = 0
    for idx, n in enumerate(openList):
        n_cost = mathod.cost(n, state_dst) + g[np.array2string(n)]
        if n_cost < min_cost:
            min_cost = n_cost
            min_idx = idx
    next_state = openList[min_idx].copy()
    del openList[min_idx]  # 删除指定状态
    return next_state


def closeList_add(state):
    for i in closeList:
        if (state == i).all():
            return
    closeList.append(state)


def delete_the_head():
    # 第一次去除头结点
    openList.clear()
    return True


# 初始化变量
iter = 0  # 迭代次数
max_iter = 10000  # 如果大于10000就退出
openList = []
# 拿到首state
openList.append(head)
g = {}  # 通过字典动态管理g
g_plus = 0.1  # g的增长速度
g[np.array2string(head)] = 0  # 首节点g为0
# close表
closeList = []
# 使用方法1
mathod = Mathod(4)
# 现在的状态
state_now = head
# 清除头结点
exist_head = True

if __name__ == "__main__":

    # 如果无解则退出
    check_if_sulotion()
    time_start = time.time()
    while True:
        iter += 1
        # 显示当前迭代次数
        print(f"\r now is {iter} iter", end=" ")
        # 检查是否应该退出程序
        check_if_exit()

        # 清除第一次的头结点
        if exist_head and delete_the_head():
            exist_head = False

        # 检查是否找到目的节点
        check_if_finish()

        # 将上一状态加入到close表
        closeList_add(state_now.copy())

        # 拓展openList 同时得到下一个state
        state_now = expand_and_get_openList()
