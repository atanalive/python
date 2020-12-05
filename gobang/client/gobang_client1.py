#!/usr/bin/python
# _*_ coding:utf-8 _*_
debug = False
import socket
import gobang1
if debug == True:
    import sys
    print(sys.path)
# 创建一个socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接
s.connect(("127.0.0.1", 9000))
other_x = -1
other_y = 0

while True:

    # 进行one step，并发送给客户端
    receive = gobang1.game_step(other_x, other_y, -1)
    if receive == True:
        s.send("over".encode("utf-8"))
        gobang1.put_text("White chess player win !!!")
        if debug == True:
            print("over1")
        break
    if receive:
        loc = [i for i in receive]
        loc_str = f"{loc[0]} {loc[1]}"
        # 为客户端返回坐标信息
        s.send(loc_str.encode("utf-8"))

    res = s.recv(1024)
    other_loc = res.decode("utf-8")
    if other_loc == "over":
        gobang1.put_text("Black chess player win !!!")
        if debug == True:
            print("over2")
        break

    list_loc = other_loc.split(" ")
    if len(list_loc) == 2:
        other_x, other_y = list_loc[0], list_loc[1]
        other_x, other_y = int(other_x), int(other_y)
        if debug == True:
            print(other_x, other_y)

# 防止关闭窗口
while True:
    pass
# 关闭会话连接
s.close()
