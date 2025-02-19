import os
import re

filename = "student.txt"
def main():
    ctrl = True       #标记是否退出系统
    while(ctrl):
        menu()
        option = input("请选择:")
        option_str = re.sub("\D","", option)
        if option_str in ['0', '1', '2', '3', '4', '5', '6', '7']:
            option_int = int(option_str)
            if option_int == 0:
                print("退出学生信息管理系统")
                ctrl = False
            elif option_int == 1:   #录入
                insert()
            elif option_int == 2:   #查找
                search()
            elif option_int == 3:   #删除
                delete()
            elif option_int == 4:   #修改
                modify()
            elif option_int == 5:   #排序
                sort()
            elif option_int == 6:   #统计学生总数
                total()
            elif option_int == 7:   #显示所有学生信息
                show()

#输出菜单
def menu():
    print("""
    -----------学生信息管理系统----------
    --------------功能菜单--------------
    1录入学生信息
    2查找学生信息
    3删除学生信息
    4修改学生信息
    5排序
    6统计学生总人数
    7显示所有学生信息
    0退出系统
    ----------------------------------
    说明：通过数字键选择菜单
    """)

#将学生信息保存到文件
def save(student):
    try:
        student_txt = open(filename, 'a')     #以追加模式打开
    except Exception as e:
        student_txt = open(filename, 'w')    #文件不存在，创建文件打开
    for info in student:
        student_txt.write(str(info) + "\n")  #按行存储，添加换行符
    student_txt.close()                      #关闭文件

def insert():
    studentList = []
    mark = True                             #是否继续添加
    while(mark):
        id = input("请输入ID(如1001):")
        if not id:
            break
        name = input("请输入名字:")
        if not name:
            break
        try:
            english =int(input("请输入英语成绩:"))
            python = int(input("请输入python成绩:"))
            c = int(input("请输入C语言成绩:"))
        except:
            print("输入无效，不是整型类型...重新录入")
            continue
        #将输入学生信息保存到字典
        student = {"id" : id, "name" : name, "english" : english, "python" : python, "c" : c}
        studentList.append(student)
        input_mark = input("是否继续添加(y/n):")
        if input_mark == "y":
            mark = True
        else:
            mark = False
    save(studentList)  #将学生信息保存到文件
    print("学生信息录入完毕")

def delete():
    mark = True
    while mark:
        show()
        studetId = input("请输入学生ID:")
        if studetId != "":
            if os.path.exists(filename):
                with open(filename, 'r') as rfile:
                    student_old = rfile.readlines()       #读取全部内容
            else:
                student_old = []
            ifdel = False
            if student_old:
                with open(filename, 'w') as wfile:
                    d = {}
                    for list in student_old:
                        d = dict(eval(list))
                        if d['id'] != studetId:
                            wfile.write(str(d) + "\n")
                        else:
                            ifdel = True
                    if ifdel:
                        print("ID为 %s 的学生信息已被删除" %studetId)
                    else:
                        print("没有ID为 %s 的学生信息" %studetId)
            else:
                print("无学生信息")
                break
            show()
            input_mark = input("是否继续删除(y/n):")
            if input_mark == "y":
                mark = True
            else:
                mark = False
#修改学生信息
def modify():
    show()
    if os.path.exists(filename):
        with open(filename, 'r') as rfile:
            student_old = rfile.readlines()
    else:
        return
    studentid = input("请输入要修改学生的ID:")
    with open(filename, 'w') as wfile:
        for student in student_old:
            d = dict(eval(student))
            if d["id"] == studentid:
                print("找到了这名学生，可以修改他的信息")
                while True:
                    try:
                        d["name"] = input("请输入姓名:")
                        d["english"] = int(input("请输入英语成绩:"))
                        d["python"] = int(input(("请输入python成绩:")))
                        d["c"] = int(input("请输入C语言成绩:"))
                    except:
                        print("输入无效，不是整型类型...重新输入")
                    else:
                        break
                student = str(d)
                wfile.write(student+ "\n")
                print("修改成功")
            else:
                wfile.write(student)  #将为修改的信息写入文件
    mark = input("是否继续修改(y/n):")
    if mark == "y":
        modify()

def search():
    mark = True
    student_query = []        #保存查询结果
    while mark:
        id = ""
        name = ""
        if os.path.exists(filename):
            mode = input("请输入查询模式(1.按ID查询 2.按姓名查询):")
            if mode == "1":
                id = input("请输入要查询的学生ID:")
            elif mode == "2":
                name = input("请输入要查询的学生姓名:")
            else:
                print("输入无效，请重新输入")
                search()
            with open(filename, 'r') as file:
                student = file.readlines()
                for list in student:
                    d = dict(eval(list))
                    if id != "":
                        if d["id"] == id:
                            student_query.append(d)
                    elif name != "":
                        if d["name"] == name:
                            student_query.append(d)
                show_student(student_query)    #显示查询结果
                student_query.clear()
                input_mark = input("是否继续查询(y/n):")
                if input_mark == "y":
                    mark = True
                else:
                    mark = False

        else:
            print("无学生信息")
            return

#将保存到列表中的学生信息显示出来
def show_student(studentList):
    if not studentList:
        print("无数据信息")
        return
    #定义标题显示格式
    format_title = "{:^6}{:^12}\t{:^8}\t{:^10}\t{:^10}\t{:^10}"
    print(format_title.format("ID", "姓名", "英语成绩", "python成绩", "C语言成绩", "总成绩"))

    #定义具体内容显示格式
    format_data = "{:^6}{:^12}\t{:^12}\t{:^10}\t{:^10}\t{:^10}"
    for info in studentList:
        print(format_data.format(info.get("id"),
                                 info.get("name"),str(info.get("english")),str(info.get("python")),
                                 str(info.get("c")),
                                 str(info.get("english") + info.get("python") + info.get("c")).center(12)))

#实现统计学生人数总数
def total():
    if os.path.exists(filename):
        with open(filename, 'r') as rfile:
            student_old = rfile.readlines()
            if student_old:
                print("一共有 %d 名学生" %len(student_old))
            else:
                print("还没录入学生信息")
    else:
        print("暂时未保存数据信息")

def show():
    student_new = []
    if os.path.exists(filename):
        with open(filename, 'r') as rfile:
            student_old = rfile.readlines()
        for list in student_old:
            student_new.append(eval(list))
        if student_new:
            show_student(student_new)
        else:
            print("暂未保存数据信息")

def sort():
    show()
    if os.path.exists(filename):
        with open(filename, 'r') as rfile:
            student_old = rfile.readlines()
            student_new = []
        for list in student_old:
            d = dict(eval(list))
            student_new.append(d)
    else:
        return
    ascORdesc = input("请选择排序方式(1.升序 2.降序):")
    if ascORdesc == "1":
        ascORescBool = False
    elif ascORdesc == "2":

        ascORescBool = True
    else:
        print("输入有误，请重新输入")
        sort()
    mode = input("请选择排序方式(1.按ID排序  2.按英语成绩排序 3.按python成绩排序 4.按C语言成绩排序 5.按总成绩排序):")
    if mode == "1":
        student_new.sort(key=lambda x : x["id"], reverse=ascORescBool)
    elif mode == "2":
        student_new.sort(key=lambda x : x["english"], reverse=ascORescBool)
    elif mode == "3":
        student_new.sort(key= lambda x : x["python"], reverse=ascORescBool)
    elif mode == "4":
        student_new.sort(key= lambda x : x["c"], reverse=ascORescBool)
    elif mode == "5":
        student_new.sort(key= lambda x : x["english"] + x["python"] + x["c"], reverse=ascORescBool)
    else:
        print("输入有误，请重新输入")
        sort()
    show_student(student_new)


if __name__ == '__main__':
    main()