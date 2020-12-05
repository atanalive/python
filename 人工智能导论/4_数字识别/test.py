import numpy as np

x = np.arange(12).reshape(3, 4)
y = np.arange(3).reshape(3, 1)
# x = np.where(x > 5, x, 0)
# y = np.where(x > 0, 1, 0)
#
# print(np.sqrt(6 / 4))
# for i in range(20):
#     print(np.random.uniform(-np.sqrt(6 / 4),np.sqrt(6 / 4)))
# one = np.ones([10])
# idx = np.argwhere(one == 1)
# idx=np.squeeze(idx.T)
x[2,2] = 100
# print(idx)
# print()
# print(one)
print(x)
print(np.argmax(x))
# print(y)
# print(x * y)
# print(np.exp(x) / np.exp(x).sum())
# print(x @ y)
