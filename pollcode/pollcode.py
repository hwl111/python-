import os, time, string, random, tkinter, qrcode
from pystrich.ean13 import EAN13Encoder
import tkinter.filedialog
import tkinter.messagebox
from tkinter import *
from string import digits

root = tkinter.Tk()       #tkinter模块为python的标准图像界面接口,建立根窗口
number = "123456789"
letter = "ABCDEFGHIJKLMNPQRSTUVWXYZ1234567890"
allis = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+"
i = 0
randstr = []
fourth = []
fifth = []
randfir = ""
randsec = ""
randthr = ""
str_one = ""
strone = ""
strtwo = ""
nextcard = ""
userput = ""
nres_letter = ""

"""
mkdir() 判断保存伪码的codepath文件夹是否存在，不存在则创建
openfile() 读取文本文件函数，主要读取保存产品编号和生成数量文件mrsoft.mri,
         以及用户选择已生成的文件编码
inputbox() 输入验证判断函数，根据参数判断输入的是那种类型，是否合法
wfile() 编码输出显示函数，通过屏幕输出和文件输出两种方式生成防伪码信息
"""



#判断保存伪码的codepath文件夹是否存在，不存在则创建
def mkdir(path):
    isexists = os.path.exists(path)
    if  not isexists:
        os.mkdir(path)

def openfile(filename):
    f = open(filename)
    flist = f.read()
    f.close()
    return flist

def inputbox(showstr, showorder, length):
    instr = input(showstr)  #showstr为输入提示文字
    #分成三种验证方式验证：1.数字不限位数 2.字母 3.数字且有位数要求
    if len(instr) != 0:
        if showorder == 1:    #验证方式1,数字格式:不限位数,大于0的整数
            if str.isdigit(instr):
                if instr == 0:
                    print("\033[1;31;40m 输入为0,请重新输入！！\033[0m")
                    return "0"
                else:
                    return instr
            else:
                print("\033[1;31;40m 非法输入,请重新输入！！\033[0m")
                return "0"
        if showorder == 2:
            if str.isalpha(instr):
                if len(instr) != length:  #判断输入位数
                    print("\033[1;31;40m必须输入"+str(length) + "个字母,请重新输入！！\033[0m")
                    return "0"
                else:
                    return instr
            else:
                print("\033[1;31;40m 非法输入,请重新输入！！\033[0m")
                return "0"
        if showorder == 3:
            if str.isdigit(instr):
                if len(instr) != length:
                    print("\033[1;31;40m必须输入" + str(length) + "个数字,请重新输入！！\033[0m")
                    return "0"
                else:
                    return instr
            else:
                print("\033[1;31;40m 非法输入,请重新输入！！\033[0m")
                return "0"
    else:
        print("\033[1;31;40m 输入为空,请重新输入！！\033[0m")
        return "0"


def wfile(sstr, sfile, typeis, smsg, datapath):
    mkdir(datapath)    #调用该函数创建文件夹
    datafile = datapath + "\\" + sfile
    file = open(datafile, 'w')
    wrlist = sstr
    pdata = ""
    wdata = ""
    for i in range(len(wrlist)):  # 按条循环读取防伪码数据
        wdata = str(wrlist[i].replace('[', '')).replace(']', '')  # 去掉字符的中括号
        wdata = wdata.replace(''''','').replace(''''', '')  # 去掉字符的引号
        file.write(str(wdata))  # 写入保存防伪码的文件
        pdata = pdata + wdata  # 将单条防伪码存储到pdata 变量
    file.close()  # 关闭文件
    print("\033[1;31m" + pdata + "\033[0m")  # 屏幕输出生成的防伪码信息
    if typeis != "no":  # 是否显示“输出完成”的信息提示框。如果typeis的值为“no”,不现显示
        # 显示“输出完成”的信息提示框。显示信息包含方位信息码的保存路径
        tkinter.messagebox.showinfo("提示", smsg + str(len(randstr)) + "\n 防伪码文件存放位置：" + datafile)
        root.withdraw()  # 关闭辅助窗口
# 实现屏幕输出和文件输出编码信息，参数schoice设置输出的文件名称

def input_validation(insel):
    if str.isdigit(insel):
        if insel == 0:
            print("\033[1;31;40m    输入非法,请重新输入!!!\ 033[0m")
            return 0
        else:
            return insel
    else:
        print("\033[1;31;40m    输入非法,请重新输入!!!\ 033[0m")
        return 0

def scode1( schoice):
    # 调用inputbox函数对输入数据进行非空、输入合法性判断
    incount = inputbox("\033[1;32m     请输入您要生成验证码的数量:\33[0m", 1, 0)
    while int(incount) == 0:  # 如果输入为字母或数字0,则要求重新输入
        incount = inputbox("\033[1;32m     请输入您要生成验证码的数量:\33[0m", 1, 0)
    randstr.clear()       # 清空保存批量注册码信息的变量randstr
    for j in range(int(incount)):   # 根据输入的验证码数量循环批量生成注册码
        randfir = ''       # 设置存储单条注册码的变量为空
        for i in range(6):  # 循环生成单条注册码
            randfir = randfir + random.choice(number)  # 产生数字随机因子　
        randfir = randfir + "\n"   # 在单条注册码后面添加转义换行字符“\n”，使验证码单条列显示　
        randstr.append(randfir)    # 将单条注册码添加到保存批量验证码的变量randstr　
    #调用函数wfile()，实现生成的防伪码屏幕输出和文件输出
    wfile(randstr,"scode" + str(schoice) + ".txt", "", "已生成6位防伪码共计：","codepath")

#实现生成9位数字防伪码函数
def scode2(schoice):
    ordstart = inputbox("\033[1;32m    请输入系列产品的数字起始号(3位)：\33[0m",3, 3)
    while int(ordstart) == 0:
        ordstart = inputbox("\033[1;32m    请输入系列产品的数字起始号(3位)：\33[0m", 1, 0)
    ordcount = inputbox("\033[1;32m    请输入系列产品的数字起始号(3位)：\33[0m", 1, 0)
    while int(ordcount)  < 1 or int(ordcount) > 9999:
        ordcount = inputbox("\033[1;32m    请输入系列产品的数字起始号(3位)：\33[0m", 1, 0)
    incount = inputbox("\033[1;32m    请输入要生成每个系列产品的防伪码数量：\33[0m", 1, 0)
    while int(incount) == 0:
        incount = inputbox("\033[1;32m    请输入要生成每个系列产品的防伪码数量：\33[0m", 1, 0)
    randstr.clear()
    for m in range(int(ordcount)):   #分类编号产品
        for j in range(int(incount)):  #产品防伪码编号
            randfir = ""
            for i in range(6):
                randfir = randfir + random.choice(number)  #每次生成一个随机因子
            #将生成的单条防伪码添加到防伪码列表
            randstr.append(str(int(ordstart) + m) + randfir + "\n")
    #调用wfile()函数实现防伪码在屏幕输出和文件输出
    wfile(randstr, "scode", str(choice) + ".txt","", "已生成9位系列防伪码共计:","codepath")



# 企业编码管理系统主菜单
def mainmenu():
    # os.system("clear")
    print("""\033[1;35m
      ****************************************************************
                            企业编码生成系统
      ****************************************************************
          1.生成6位数字防伪编码 （213563型）
          2.生成9位系列产品数字防伪编码(879-335439型)
          3.生成25位混合产品序列号(B2R12-N7TE8-9IET2-FE35O-DW2K4型)
          4.生成含数据分析功能的防伪编码(5A61M0583D2)
          5.智能批量生成带数据分析功能的防伪码
          6.后续补加生成防伪码(5A61M0583D2)
          7.EAN-13条形码批量生成
          8.二维码批量输出          
          9.企业粉丝防伪码抽奖
          0.退出系统
      ================================================================
      说明：通过数字键选择菜单
      ================================================================
    \033[0m""")


# 通过循环控制用户对程序功能的选择
while i < 9:
    # 调入程序主界面菜单
    mainmenu()
    # 键盘输入需要操作的选项
    choice = input("\033[1;32m     请输入您要操作的菜单选项:\33[0m")
    if len(choice) != 0:  # 输入如果不为空
        choice = input_validation(choice)  # 验证输入是否为数字
        if choice == 1:
           scode1( str(choice))      # 如果输入大于零的整数，调用scode1()函数生成注册码
        # 选择菜单2,调用scode2()函数生成9位系列产品数字防伪编码
        if choice == 2:
            scode2(choice)
        # 选择菜单3,调用scode3()函数生成25位混合产品序列号
        if choice == 3:
            scode3(choice)
        # 选择菜单4,调用scode4()函数生成含数据分析功能的防伪编码
        if choice == 4:
            scode4(choice)
        # 选择菜单5,调用scode5()函数智能批量生成带数据分析功能的防伪码
        if choice == 5:
            scode5(choice)
        # 选择菜单６,调用scode6()函数后续补加生成防伪码
        if choice == 6:
            scode6(choice)
        # 选择菜单7,调用scode7()函数批量生成条形码
        if choice == 7:
          scode7( choice)
        # 选择菜单8,调用scode8()函数批量生成二维码
        if choice == 8:
            scode8( choice)
        # 选择菜单9,调用scode9()函数生成企业粉丝抽奖程序
        if choice == 9:
            scode9( choice)
        # 选择菜单0,退出系统
        if choice == 0:
            i = 0
            print("正在退出系统!!")
            break
    else:
        print("\033[1;31;40m    输入非法，请重新输入！！\033[0m")
        time.sleep(2)
