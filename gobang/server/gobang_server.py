#!/usr/bin/python
# _*_ coding:utf-8 _*_
debug = False
import socket

if debug == True:
    import sys

    print(sys.path)
import gobang

gobang.game_init()

# 创建socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定端口和id 127.0.0.1是监听本机 0.0.0.0是监听整个网络
s.bind(("127.0.0.1", 9000))
# 开始TCP监听
# 若括号中有值表示对tcp连接的优化
s.listen()
other_x = 0
other_y = 0
while True:  # 循环为多个客户端服务
    if debug == True:
        print("wait for data...")
    # res表示接收的数据流，addr表示客户端的地址
    res, addr = s.accept()  # 在这里会等待接收数据
    while True:  # 循环为一个客户端多次服务
        # 接收客户端发送信息并打印
        msg = res.recv(1024)
        if not msg:
            break

        other_loc = msg.decode("utf-8")
        if other_loc == "over":
            gobang.put_text("White chess player win !!!")
            if debug == True:
                print("over1")
            break
        list_loc = other_loc.split(" ")
        if len(list_loc) == 2:
            other_x, other_y = list_loc[0], list_loc[1]
            other_x, other_y = int(other_x), int(other_y)
            if debug == True:
                print(other_x, other_y)

        # 进行one step，并发送给客户端
        receive = gobang.game_step(other_x, other_y, 1)
        if receive == True:
            res.send("over".encode("utf-8"))
            gobang.put_text("Black chess player win !!!")
            if debug == True:
                print("over2")
            break
        if receive:
            loc = [i for i in receive]
            loc_str = f"{loc[0]} {loc[1]}"
            if debug == True:
                print(loc_str)
            # 为客户端返回坐标信息
            res.send(loc_str.encode("utf-8"))
            if debug == True:
                print(msg.decode("utf-8"))
    # 关闭本次通信 关闭客户套接字
    res.close()
# 关闭链接 关闭服务器套接字（可选）
s.close()
