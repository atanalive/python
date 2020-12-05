#!/usr/bin/python
# _*_ coding:utf-8 _*_
import pygame, sys
import numpy as np
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (700, 100)

pygame.init()

cell_size = 40  # 方格大小
board_size = 15  # a棋盘大小
bk_color = (245, 222, 179)  # 原木色
line_color = (160, 82, 45)  # 深棕色
space = 8  # 棋盘边缘距离
chess = np.zeros((board_size, board_size))  # 记录棋子，白色为1，黑色为-1


# 画棋盘
def draw_chessborad(screen):
    screen.fill(bk_color)
    # 竖线
    for i in range(board_size):
        pygame.draw.line(screen, line_color, (space + cell_size * i, space),
                         (space + cell_size * i, space + cell_size * (board_size - 1)))
    # 横线
    for i in range(board_size):
        pygame.draw.line(screen, line_color, (space, space + cell_size * i),
                         (space + cell_size * (board_size - 1), space + cell_size * i))
    # 画定位点
    pygame.draw.circle(screen, line_color, (space + cell_size * 3, space + cell_size * 3), 5)
    pygame.draw.circle(screen, line_color, (space + cell_size * 3, space + cell_size * 11), 5)
    pygame.draw.circle(screen, line_color, (space + cell_size * 11, space + cell_size * 3), 5)
    pygame.draw.circle(screen, line_color, (space + cell_size * 11, space + cell_size * 11), 5)
    pygame.draw.circle(screen, line_color, (space + cell_size * 7, space + cell_size * 7), 5)


# 画棋子
def draw_chess(x, y, screen, who):
    if who == 1:
        #  converr_alpha()提高 blit 的速度，同时实现透明效果
        white_chess = pygame.image.load("image/white_chess.png")
        screen.blit(white_chess, (space + x * cell_size - 18, space + y * cell_size - 18))
    elif who == -1:
        black_chess = pygame.image.load("image/black_chess.png")
        screen.blit(black_chess, (space + x * cell_size - 18, space + y * cell_size - 18))


# 画棋盘和棋子
def draw_board_and_chess(chess, screen):
    draw_chessborad(screen)
    for i in range(board_size):
        for j in range(board_size):
            draw_chess(i, j, screen, chess[i, j])


# 判断游戏结束
def game_over():
    # 1判断白色有没有获胜
    if who_win(1) == True:
        put_text("White chess player win !!!")
        return True
    # -1判断黑色有没有获胜
    if who_win(-1) == True:
        put_text("Black chess player win !!!")
        return True
    # 如果棋盘满了则游戏结束
    if full_board() == True:
        put_text("Game Over!!!")
        return True

def full_board():
    # 如果找到0就没有满
    for i in range(board_size):
        for j in range(board_size):
            if chess[i, j] == 0:
                return False
    # 如果找到0则表示棋盘满了
    return True


# 1判断白色有没有获胜，-1判断黑色有没有获胜
def who_win(who):
    # 判断水平和竖直方向
    count_x = 0
    count_y = 0
    for i in range(board_size):
        for j in range(board_size):
            # 如果五连则返回真
            if count_x == 5 or count_y == 5:
                return True
            # 判断行
            # 如果该子为who 计数加一
            if chess[i, j] == who:
                count_x += 1
            # 如果不为who x方向计数中断，
            else:
                count_x = 0
            # 判断列
            if chess[j, i] == who:
                count_y += 1
            else:
                count_y = 0
        # 一行或者一列结束清除计数
        count_x = 0
        count_y = 0

    # 判断斜方向
    count_slash = 0
    # 判断反斜线 /
    # 左上部分
    for i in range(4, board_size):
        j = 0
        while i >= 0:
            if count_slash == 5:
                return True
            if chess[i, j] == who:
                count_slash += 1
            else:
                count_slash = 0
            i -= 1
            j += 1
        # 一条斜线找完了清零
        count_slash = 0
    # 右下部分
    for j in range(1, board_size - 4):
        i = board_size - 1
        while j < board_size:
            if count_slash == 5:
                return True
            if chess[i, j] == who:
                count_slash += 1
            else:
                count_slash = 0
            i -= 1
            j += 1
        # 一条斜线找完了清零
        count_slash = 0

    # 判断 斜线 \
    # 左下部分
    for i in range(0, board_size - 4):
        j = 0
        while i < board_size:
            if count_slash == 5:
                return True
            if chess[i, j] == who:
                count_slash += 1
            else:
                count_slash = 0
            i += 1
            j += 1
        # 一条斜线找完了清零
        count_slash = 0
    # 右上部分
    for j in range(1, board_size - 4):
        i = 0
        while j < board_size:
            if count_slash == 5:
                return True
            if chess[i, j] == who:
                count_slash += 1
            else:
                count_slash = 0
            i += 1
            j += 1
        # 一条斜线找完了清零
        count_slash = 0


chess_x = 0
chess_y = 0


def mouse_put_chess(x, y, who):
    global chess_x, chess_y
    # 处理落子 -10是为了处理鼠标落点，因为x，y鼠标是根部的坐标，处理成顶部的坐标
    chess_x = int((x + cell_size / 2 - 10) // cell_size)
    chess_y = int((y + cell_size / 2 - 10) // cell_size)
    if chess[chess_x, chess_y] != 0:
        return False
    chess[chess_x, chess_y] = who
    return True

# 显示字体设置
def draw_text(string):
    pygame.font.init()
    font = pygame.font.Font("C:\\Windows\\Fonts\\simkai.ttf", 30)
    text = font.render(string, True, (210,105,30))
    return text

# step后等待对面走子的显示字体
def put_text(string,loc=(100, 250)):
    screen = pygame.display.set_mode(
        (space * 2 + cell_size * (board_size - 1), space * 2 + cell_size * (board_size - 1)))
    # 画棋盘
    draw_board_and_chess(chess, screen)
    screen.blit(draw_text(string),loc)
    # 更新画面
    pygame.display.update()

# 装饰器 为了显示字体
def after_step(func):
    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        put_text("wait for the other player !!!")
        return f
    return wrapper


@after_step
def game_step(other_x, other_y, who):
    if other_x != -1:
        chess[other_x, other_y] = -1 * who
    while True:
        screen = pygame.display.set_mode(
            (space * 2 + cell_size * (board_size - 1), space * 2 + cell_size * (board_size - 1)))
        if who == 1:
            pygame.display.set_caption("white plarer")
        else:
            pygame.display.set_caption("black plarer")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 在调用sys.exit()终止程序之前，总是应该先调用pygame.quit()。通常，由于程序退出之前，
                # Python总是会关闭pygame，这不会真的有什么问题。但是，在IDLE中有一个bug，如果一个
                # Pygame程序在调用pygame.quit()之前就终止了，将会导致IDLE挂起。
                pygame.quit()
                sys.exit()
        mouse=pygame.mouse.get_pressed()
        if mouse[0]: # 如果左键被按下
            if mouse_put_chess(*pygame.mouse.get_pos(), who):
                # 判断游戏是否结束
                game_over()
                # 画棋盘
                draw_board_and_chess(chess, screen)
                # 更新画面
                pygame.display.update()

                global chess_x, chess_y
                return chess_x, chess_y

        # 判断游戏是否结束
        if game_over():
            return True
        # 画棋盘
        draw_board_and_chess(chess, screen)
        # 更新画面
        pygame.display.update()


if __name__ == "__main__":
    while True:
        receive = game_step(5, 5, 1)
        if receive:
            print(receive)
            loc = [i for i in receive]
            loc_str = f"{loc[0]},{loc[1]}"
            print(loc_str)
