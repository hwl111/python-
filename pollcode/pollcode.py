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

# 输入数字验证，判断输入是否在0-9之间的整数
def input_validation(insel):
    if str.isdigit(insel):
        insel = int(insel)
        # if insel == 0:
        #     # print("\033[1;31;40m    输入非法，请重新输入！！\033[0m")
        #     return 0
        # else:
        #     return insel
        return insel
    else:
        print("\033[1;31;40m       输入非法，请重新输入！！\033[0m")
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
    wfile(randstr, "scode" + str(schoice) + ".txt", "", "已生成9位系列产品防伪码共计：","codepath")


def scode3(schoice):                       #生成25位混合产品序列号函数,参数schoice设置输出文件名称
    #输入要生成的防伪码数量
    incount = inputbox("\033[1;32m    请输入要生成的25位混合产品序列号数量：\33[0m", 1, 0)
    while int(incount) == 0:
        incount = inputbox("\033[1;32m    请输入要生成的25位混合产品序列号数量：\33[0m", 1, 0)
    randstr.clear()
    for j in range(int(incount)):
        strone = ""           #保存生成的单条防伪码,不带横线"-",循环时清空
        for i in range(25):
            #每次产生一个随机因子,也就是每次生成单条防伪码一位
            strone = strone +random.choice(letter)
        #将生成的防伪码隔5位添加'-'
        strtwo = strone[:5] + "-" + strone[5:10] + "-" + strone[10:15] + "-" + strone[15:20] + "-" + strone[20:25] + "\n"
        randstr.append(strtwo)  #将生成的单条防伪码添加到防伪码列表
    #调用wfile()函数实现防伪码在屏幕输出和文件输出
    wfile(randstr, "scode" + str(schoice) + ".txt", "", "已生成25位混合产品序列号共计：","codepath")

def scode4(schoice):        #生成含数据分析功能防伪编码参数
    intype = inputbox("\033[1;32m    请输入数据分析编号(3位字母)：\33[0m", 2, 3)
    #验证输入是否是三个字母
    while not str.isalpha(intype) or len(intype) != 3:
        intype = inputbox("\033[1;32m    请输入数据分析编号(3位字母)：\33[0m", 2, 3)
    incount = inputbox("\033[1;32m    请输入要生成的带数据分析功能的防伪码数量：\33[0m", 1, 0)
    #验证输入是否大于0
    while int(incount) == 0:
        incount = inputbox("\033[1;32m    请输入要生成的带数据分析功能的防伪码数量：\33[0m", 1, 0)
    ffcode(incount, intype, "", schoice)         #调用ffcode()函数生成防伪码

# 生成含数据分析功能防伪编码函数，参数scount为要生成的防伪码数量，typestr为数据分析字符
# 参数ismessage在输出完成时是否显示提示信息，为“no”不显示，为其他值显示；参数schoice设置输出的文件名称
def ffcode(scount, typestr,ismessage, schoice):
    randstr.clear()  # 清空保存批量注册码信息的变量randstr
    # 按数量生成含数据分析功能注册码
    for j in range(int(scount)):
        strpro = typestr[0].upper()    # 取得三个字母中的第一个字母，并转为大写，区域分析码
        strtype = typestr[1].upper()   # 取得三个字母中的第二个字母，并转为大写，颜色分析码
        strclass = typestr[2].upper()  # 取得三个字母中的第三个字母，并转为大写，版本分析码
        randfir = random.sample(number, 3)  # 随机抽取防伪码中的三个位置，不分先后
        randsec = sorted(randfir)  # 对抽取的位置进行排序并存储给randsec变量，以便按顺序排列三个字母的位置
        letterone = ""    # 清空存储单条防伪码的变量letterone
        for i in range(9):  # 生成9位的数字防伪码
            letterone = letterone + random.choice(number)
        # 将三个字母按randsec变量中存储的位置值添加到数字防伪码中，并放到sim变量中
        sim = str(letterone[0:int(randsec[0])]) + strpro + str(
            letterone[int(randsec[0]):int(randsec[1])]) + strtype + str(
            letterone[int(randsec[1]):int(randsec[2])]) + strclass + str(letterone[int(randsec[2]):9]) + "\n"
        randstr.append(sim)   # 将组合生成的新防伪码添加到randstr变量
    # 调用wfile()函数，实现生成的防伪码屏幕输出和文件输出
    wfile(randstr, typestr + "scode" + str(schoice) + ".txt", ismessage, "生成含数据分析防伪码共计：","codepath")

#智能批量生产带数据分析功能的防伪码
def scode5(schoice):
    default_dir = r"codeauto.mri"   #设置默认打开的文件名
    # 打开文件选择对话框，指定打开的文件名称为"mrsoft.mri" ，扩展名为“mri”，可以使用记事本打开和编辑
    file_path = tkinter.filedialog.askopenfilename(filetypes=[("Text file", "*.mri")],
                                                   title=u"请选择自动防伪码智能批处理文件：",
                                                   initialdir=(os.path.expanduser(default_dir)))
    codelist = openfile(file_path)
    #以换行符为分隔符将读取的幸喜转换成列表
    codelist = codelist.split("\n")
    print(codelist)
    for item in codelist:
        codea = item.split(",")[0]
        codeb = item.split(",")[1]
        ffcode(codeb, codea, "no", schoice)

#实现防伪码的补充生成功能,避免生成的防伪码重复
def scode6(schoice):
    default_dir = r"c:\ABDscode5.txt"  #设置默认打开文件名称
    # 按默认的文件名称打开文件选择对话框，用于打开已经存在的防伪码文件
    file_path = tkinter.filedialog.askopenfilename(title=u"请选择已经生成的防伪码文件",
                                                   initialdir=(os.path.expanduser(default_dir)))
    codelist = openfile(file_path)
    codelist = codelist.split("\n")
    codelist.remove("")    #删除列表中的空行
    strset = codelist[0]   #读取一行数据,以便获取原验证码的字母标注信息
    #用makestrans()方法创建删除数字的字符映射转换表
    remove_digits = str.maketrans("", "", digits)
    #用translate()方法删除数字
    res_leter = strset.translate(remove_digits)
    nres_letter = list(res_leter)
    strpro = nres_letter[0]
    strtype = nres_letter[1]
    strclass = nres_letter[2]
    #去除信息中的括号和引号
    nres_letter = strpro.replace(''''','').replace(''''', '') + strtype.replace(
        ''''','').replace(''''', '') + strclass.replace(''''','').replace(''''', '')
    card = set(codelist)
    #利用tkinter的messagebox提示用户之前生成的防伪码数量
    tkinter.messagebox.showinfo("提示", "原验证码共计" + str(len(card)))
    root.withdraw()  #关闭提示信息框
    incount = inputbox("请输入补充生成防伪码数量:", 1, 0)
    #最大输入生成数量2倍的新防伪码
    for j in range(int(incount) * 2):
        randfir = random.sample(number, 3)
        randsec = sorted(randfir)
        addcount = len(card)
        strone = ""
        for i in range(9):
            strone = strone + random.choice(number)
            # 将三个字母按randsec变量中存储的位置值添加到数字防伪码中，并放到sim变量中
            sim = str(strone[0:int(randsec[0])]) + strpro + str(
                strone[int(randsec[0]):int(randsec[1])]) + strtype + str(
                strone[int(randsec[1]):int(randsec[2])]) + strclass + str(strone[int(randsec[2]):9]) + "\n"
            card.add(sim)
            if len(card) > addcount:
                randstr.append(sim)
                addcount = len(card)
            if len(card) >= int(incount):
                print(len(randstr))
                break
        # 调用wfile()函数，实现生成的防伪码屏幕输出和文件输出
    wfile(randstr, nres_letter + "ncode" + str(choice) + ".txt", nres_letter, "生成后补防伪码共计：", "codeadd")

#实现条形码的输出
def scode7(schoise):
    mainid = inputbox("\033[1;32m     请输入EN13的国家代码（3位） :\33[0m", 3, 3)  # 输入3位国家代码
    while int(mainid) < 1 or len(mainid) != 3:   # 验证输入是否为3位数字（转为整数后小于1和长度不等于3，重新输入）
         mainid = inputbox("\033[1;32m     请输入EAN13的国家代码（3位）::\33[0m", 1, 0)
    compid = inputbox("\033[1;32m     请输入EAN13的企业代码（4位）:\33[0m", 3, 4)  # 输入4位企业代码
    while int(compid) < 1 or len(compid) != 4:   # 验证输入是否为4位数字
         compid = inputbox("\033[1;32m     请输入EAN13的企业代码（4位）:\33[0m", 1, 0)
    incount = inputbox("\033[1;32m     请输入要生成的条形码数量:\33[0m", 1, 0)  # 输入要生成的条形码数量
    while int(incount) == 0:  # 输入信息转为整数后等于0，重新输入
        incount = inputbox("\033[1;32m     请输入要生成的条形码数量:\33[0m", 1, 0)
    mkdir("barcode")  # 判断保存条形码的文件夹是否存在，不存在，则创建该文件夹
    for j in range(int(incount)):  # 批量生成条形码
        strone = ''  # 清空存储单条条形码的变量
        for i in range(5):  # 生成条形码的6位（除国家代码、企业代码和校验位之外的6位）数字
            strone = strone + str(random.choice(number))
        barcode = mainid + compid + strone  # 把国家代码、企业代码和新生成的随机码进行组合
        # 计算条形码的校验位
        evensum = int(barcode[1]) + int(barcode[3]) + int(barcode[5]) + int(barcode[7]) + int(barcode[9]) + int(
            barcode[11])  # 偶数位
        oddsum = int(barcode[0]) + int(barcode[2]) + int(barcode[4]) + int(barcode[6]) + int(barcode[8]) + int(
            barcode[10])
        # checkbit=int(10-(evensum *3 + oddsum)%10)
        checkbit = int((10 - (evensum * 3 + oddsum) % 10) % 10)
        barcode = barcode + str(checkbit)  # 组成完整的EAN13条形码的13位数字
        print(barcode)
        encoder = EAN13Encoder(barcode)  # 调用EAN13Encoder生成条形码
        encoder.save("barcode\\" + barcode + ".png")  # 保存条形码信息图片到文件

#实现二维码的打印和输出
def scode8(schoice):
    #输入要生成的二维码的数量
    incount = inputbox("\033[1;32m     请输入要生成12位数字的二维码数量:\33[0m", 1, 0)
    while int(incount) == 0:
        incount = inputbox("\033[1;32m     请输入要生成12位数字的二维码数量:\33[0m", 1, 0)
    mkdir("qrcode")
    for j in range(int(incount)):
        strone = ""
        for i in range(12):
            strone = strone + str(random.choice(number))
        encoder = qrcode.make(strone)  #生成二维码
        encoder.save("qrcode\\" + strone + ".png") #保存二维码到图片


#实现粉丝企业抽奖
def scode9(schoice):
    default_dir = r"lottery.ini"  #设置默认打开文件位项目路径下的"lottery.ini"
    #选择包含用户抽奖信息票号的文件,扩展名为”.ini“
    file_path = tkinter.filedialog.askopenfilename(filetypes=[("Ini file","*.ini")],
                                                   title=u"请选择包含抽奖号码的抽奖文件:",initialdir=(os.path.expanduser(default_dir)))
    codelist = openfile(file_path)
    codelist = codelist.split("\n")
    #要求用户输入抽奖数量
    incount = inputbox("\033[1;32m     请输要生成的抽奖数量:\33[0m", 1, 0)
    while int(incount) == 0:
        incount = inputbox("\033[1;32m     请输要生成的抽奖数量:\33[0m", 1, 0)
    strone = random.sample(codelist, int(incount))
    for i in range(int(incount)):
        #将抽奖列表中的括号去掉
        wdata = str(strone[i].replace('[', '')).replace(']', '') # 将抽奖数列的中括号去掉
        #将抽奖列表中的引号去掉
        wdata = wdata.replace(''''','').replace(''''', '')  # 将抽奖数列的引号去掉
        print("\033[1;32m         " + wdata + "\33[0m")  # 输出中奖信息

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
