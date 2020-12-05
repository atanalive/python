import socket

# 创建socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定端口和id 127.0.0.1是监听本机 0.0.0.0是监听整个网络
s.bind(("127.0.0.1", 9000))
# 开始TCP监听
# 若括号中有值表示对tcp连接的优化
s.listen(2)

while True: # 循环为多个客户端服务
    print("wait for connect...")
    # res表示接收的数据流，addr表示客户端的地址
    res, addr = s.accept()  # 在这里会等待接收数据
    while True:  # 循环为一个客户端多次服务
        # 接收客户端发送信息并打印
        msg = res.recv(100)
        if not msg:
            break
        # 为客户端返回信息表示接收成功
        res.send(msg.upper())
        print(msg.decode("utf-8"))
    # 关闭本次通信 关闭客户套接字
    res.close()
# 关闭链接 关闭服务器套接字（可选）
s.close()
