import os
try:
    import pygame
except ModuleNotFoundError:
    print("正在安装pygame模块，请稍等...")
    os.system("pip install pygame")
import tool

if __name__ == '__main__':
    paint = tool.Paint()
    try:
        paint.run()
    except Exception as e:
        print(e)