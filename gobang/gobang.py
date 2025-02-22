
#棋盘初始化
def init_board():
    print('\033[1;37;41m---------简易五子棋游戏（控制台版）---------\033[0m')
    checkerboard = []
    for i in range(10):
        checkerboard.append([])
        for j in range(10):
            checkerboard[i].append("-")
    return checkerboard


def print_board(checkerboard):
    #打印棋盘
    print("\033[1;30;46m--------------------------------")
    print("   1  2  3  4  5  6  7  8  9  10")
    for i in range(len(checkerboard)):
        print(chr(i + ord('A')) + " ", end=' ');
        for j in range(len(checkerboard[i])):
            print(checkerboard[i][j] + " ", end=' ')
        print()
    print("--------------------------------\033[0m")


#打印胜利棋盘以及赢家
def msg(checkerboard,flagNum):
    # 输出最后胜利的棋盘
    print("\033[1;37;44m--------------------------------")
    print("   1  2  3  4  5  6  7  8  9  10")
    for i in range(len(checkerboard)):
        print(chr(i + ord('A')) + " ", end=' ')
        for j in range(len(checkerboard[i])):
            print(checkerboard[i][j] + " ", end=' ')
        print()
    print("--------------------------------\033[0m")
    # 输出赢家
    if (flagNum == -1):        #    因为一输入flagNum就会乘以-1
        print('\033[32m*棋胜利！***\033[0m')
    else:
        print('\033[32mo棋胜利！***\033[0m')

def game(finish, flagNum, checkerboard):
    while not finish:
        if flagNum == 1:
            flagch = '*'
            flagNum *= -1
            print("\033[1;37;45m请输入棋子的坐标（例如：A1）：\033[0m")
        else:
            flagch = '0'
            flagNum *= -1
            print("\033[1;37;45m请输入棋子的坐标（例如：A2）：\033[0m")
        valid_input = False  # 用来标记输入是否有效
        while not valid_input:
            str = input()
            ch = str[0]
            x = ord(ch) - ord('A')
            y = int(str[1]) - 1

            # 检查输入的坐标是否有效
            if x < 0 or x > 9 or y < 0 or y > 9:
                print("\033[1;31;40m输入错误！请重新输入！（坐标范围 A1 到 J10）\033[0m")
                continue  # 继续要求输入

            # 检查该位置是否已经有棋子
            if checkerboard[x][y] != '-':
                print("\033[1;31;40m此位置已有棋子！请重新输入！\033[0m")
                continue  # 继续要求输入

            # 如果位置合法且为空，则放置棋子并结束循环
            if checkerboard[x][y] == '-':
                checkerboard[x][y] = flagch
                valid_input = True  # 输入合法，结束循环
        print_board(checkerboard)
        finish = if_five_chess_piece(checkerboard, flagch, x, y, flagNum)

def if_five_chess_piece(checkerboard, flagch, x, y, flagNum):
    #判断左侧
    finish = False
    if (y - 4 >= 0):
        if (checkerboard[x][y-1] == flagch and checkerboard[x][y-2] == flagch and checkerboard[x][y-3] == flagch and checkerboard[x][y-4] == flagch):
            finish = True
            msg(checkerboard, flagNum)
            return finish
    #判断右侧
    if (y + 4 <= 9):
        if(checkerboard[x][y+1] == flagch and checkerboard[x][y+2] == flagch and checkerboard[x][y+3] == flagch and checkerboard[x][y+4] == flagch):
            finish = True
            msg(checkerboard, flagNum)
            return finish
    #判断上侧
    if (x - 4 >= 0):
        if(checkerboard[x-1][y] == flagch and checkerboard[x-2][y] == flagch and checkerboard[x-3][y] == flagch and checkerboard[x-4][y] == flagch):
            finish = True
            msg(checkerboard, flagNum)
            return finish
    #判断下侧
    if (x + 4 <= 9):
        if(checkerboard[x+1][y] == flagch and checkerboard[x+2][y] == flagch and checkerboard[x+3][y] == flagch and checkerboard[x+4][y] == flagch):
            finish = True
            msg(checkerboard, flagNum)
            return finish
    #判断左上侧
    if (x - 4 >= 0 and y - 4 >= 0):
        if(checkerboard[x-1][y-1] == flagch and checkerboard[x-2][y-2] == flagch and checkerboard[x-3][y-3] == flagch and checkerboard[x-4][y-4] == flagch):
            finish = True
            msg(checkerboard, flagNum)
            return finish
    #判断右上侧
    if (x - 4 >= 0 and y + 4 <= 9):
        if(checkerboard[x-1][y+1] == flagch and checkerboard[x-2][y+2] == flagch and checkerboard[x-3][y+3] == flagch and checkerboard[x-4][y+4] == flagch):
            finish = True
            msg(checkerboard, flagNum)
            return finish
    #判断左下侧
    if (x + 4 <= 9 and y - 4 >= 0):
        if(checkerboard[x+1][y-1] == flagch and checkerboard[x+2][y-2] == flagch and checkerboard[x+3][y-3] == flagch and checkerboard[x+4][y-4] == flagch):
            finish = True
            msg(checkerboard, flagNum)
            return finish
    #判断右下侧
    if (x + 4 <= 9 and y + 4 <= 9):
        if(checkerboard[x+1][y+1] == flagch and checkerboard[x+2][y+2] == flagch and checkerboard[x+3][y+3] == flagch and checkerboard[x+4][y+4] == flagch):
            finish = True
            msg(checkerboard, flagNum)
            return finish


def main():
    finish = False  #游戏是否结束
    flagNum = 1  #当前棋子颜色A1

    checkerboard = init_board()
    print_board(checkerboard)
    game(finish, flagNum, checkerboard)



if __name__ == '__main__':
    main()