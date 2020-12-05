import socket

# 创建一个socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接
s.connect(("127.0.0.1", 9000))

while True:
    # 发送消息
    str = input("please input a string:\n")
    # 发送消息
    s.send(str.encode("utf-8"))
    # 接收服务器端返回值并打印
    res = s.recv(1024)
    print(res.decode("utf-8"))
# 关闭会话连接
s.close()