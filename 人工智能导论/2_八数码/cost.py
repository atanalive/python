import numpy as np


# 计算损失
class Mathod(object):
    def __init__(self, mathod):
        self.mathod = mathod

    def cost(self, state_now, state_dst):
        # 宽度优先搜索
        if self.mathod == 0:
            return 0
        # 不在位数
        elif self.mathod == 1:
            return (state_now != state_dst).sum()
        # 距离
        elif self.mathod == 2:
            size = state_now.shape[0]
            cost = 0
            for i in range(size):
                for j in range(size):
                    for h in range(size):
                        for w in range(size):
                            if state_now[h,w] == state_dst[i, j]:
                                cost += np.abs(h - i) + np.abs(w - j)

            return cost
        elif self.mathod == 3:
            cost = 0
            cost += _reverse_pair(state_now) * 3
            return cost
        elif self.mathod == 4:
            cost = 0
            cost += (state_now != state_dst).sum()
            cost += _reverse_pair(state_now) * 3
            return cost


# 求逆数对 即每个数字与前面比它大的数字组成的数字对
def _reverse_pair(num):
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
