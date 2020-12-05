import numpy as np
from load_image import load_image
import matplotlib.pyplot as plt


class Model_Base(object):
    def __init__(self):
        self.lr = 0.01


# Alive
# 模仿torch架构，用numpy实现神经网络
class Model_numpy(Model_Base):
    def __init__(self):
        super(Model_numpy, self).__init__()
        self.l1 = Linear(63, 256)
        self.relu1 = ReLU()
        self.l2 = Linear(256, 256)
        self.relu2 = ReLU()
        self.l3 = Linear(256, 10)
        self.loss = CrossEntropyLoss(10)

    def forward(self, input: np.ndarray):
        x1 = self.relu1(self.l1(input))
        x2 = self.relu2(self.l2(x1))
        output = self.l3(x2)
        return output

    def backward(self):
        grad1 = self.loss.backward()
        grad2 = self.l3.backward(grad1)
        grad3 = self.relu2.backward(grad2)
        grad4 = self.l2.backward(grad3)
        grad5 = self.relu1.backward(grad4)
        grad6 = self.l1.backward(grad5)
        return grad6

    def __call__(self, input: np.ndarray):
        return self.forward(input)


class Linear(Model_Base):
    # input_dim: int 函数参数中的冒号是参数的类型建议符，告诉程序员希望传入的实参的类型。
    # -> 函数后面跟着的箭头是函数返回值的类型建议符，用来说明该函数返回的值是什么类型
    def __init__(self, input_dim: int, output_dim: int, if_bias: bool = True) -> None:
        # 参数初始化
        self.w_grad = 0
        self.b_grad = 0

        super(Linear, self).__init__()
        self.w = np.random.uniform(-np.sqrt(6 / (input_dim + output_dim)), np.sqrt(6 / (input_dim + output_dim)),
                                   [output_dim, input_dim])
        self.if_bias = if_bias
        if self.if_bias == True:
            self.bias = np.random.uniform(-np.sqrt(6 / (input_dim + output_dim)), np.sqrt(6 / (input_dim + output_dim)),
                                          [output_dim, 1])
        else:
            pass

    def forward(self, input: np.ndarray) -> np.ndarray:
        # 过滤类型
        if type(input) is not np.ndarray:  # 期望得到np.ndarray类型
            raise Exception("except get the type: np.ndarray")

        self.input = input
        if self.if_bias:
            # @为矩阵相乘
            output = self.w @ self.input + self.bias
        else:
            output = self.w @ self.input
        return output

    def backward(self, next_grad: np.ndarray) -> np.ndarray:
        self.w_grad = next_grad @ self.input.T
        self.b_grad = 1 * next_grad
        self.w = self.w - self.w_grad * self.lr
        self.bias = self.bias - self.b_grad * self.lr
        self.last_grad = (next_grad * self.w).sum(axis=0).reshape(len(self.input), 1)
        return self.last_grad

    # 调用实例时默认调用该函数
    def __call__(self, input: np.ndarray):
        return self.forward(input)


class ReLU(Model_Base):
    def __init__(self):
        super(ReLU, self).__init__()

    def forward(self, input: np.ndarray):
        if type(input) is not np.ndarray:  # 期望得到np.ndarray类型
            raise Exception("except get the type: np.ndarray")
        self.output = np.where(input > 0, input, 0)
        return self.output

    def backward(self, next_grad):
        relu_grad = np.where(self.output > 0, 1, 0)
        last_grad = next_grad * relu_grad
        return last_grad

    def __call__(self, input: np.ndarray):
        return self.forward(input)


class CrossEntropyLoss(Model_Base):
    def __init__(self, output_dim):
        self.one_hot_size = output_dim
        self.y_hat = np.zeros((self.one_hot_size, 1))
        super(Model_Base, self).__init__()

    def forward(self, input, target):
        self.target = target
        y = self.soft_max(input)
        self.y_hat[target] = 1
        loss = -(self.y_hat * np.log(y)).sum()
        return loss

    def backward(self):
        last_grad = self.a_i - self.y_hat
        # 重置y_hat
        self.y_hat[self.target] = 0
        return last_grad

    def soft_max(self, input):
        output = np.exp(input) / np.exp(input).sum()
        self.a_i = output
        return output

    def __call__(self, input, target):
        return self.forward(input, target)


data = []
# 加载数字
load_number = load_image()
if __name__ == '__main__':
    net = Model_numpy()
    # train data
    for i in range(10000):
        output = net(load_number(i % 10).reshape(63, 1))
        loss = net.loss(output, i % 10)

        net.backward()
        # print(loss)
        data.append(loss)

    # test data handle
    correct = 0
    total = 0
    one_to_zero = 3
    zero_to_one = 3
    for i in range(1000):
        img = load_number(i % 10).reshape(63, 1).copy()
        # one_to_zero
        idx = np.squeeze(np.argwhere(np.squeeze(img.T) == 1).T)
        choose_idx = np.random.choice(idx, one_to_zero, replace=False)
        for j in choose_idx:
            img[j, 0] = 0
        # zero_to_one
        idx = np.squeeze(np.argwhere(np.squeeze(img.T) == 0).T)
        choose_idx = np.random.choice(idx, one_to_zero, replace=False)
        for j in choose_idx:
            img[j, 0] = 1

        output = net(img)
        if np.argmax(output) == i % 10:
            correct += 1
        total += 1
    print(f'''
    correct is {float(correct) * 100 / total} %
    ''')

    # draw the data
    plt.style.use("ggplot")
    plt.plot(range(len(data)), data, label="loss", color="blue")
    plt.show()
