from tkinter import *

class gui_info():
    def __init__(self):
        self.master=Toplevel()
        self.master.title('使用说明')

        self.jiekou_one=StringVar()
        self.jiekou_two=StringVar()
        self.jiekou_three=StringVar()
        self.jiekou_four=StringVar()

        #############
        sw = self.master.winfo_screenwidth()
        # 得到屏幕宽度
        sh = self.master.winfo_screenheight()
        # 得到屏幕高度
        ww = 650
        wh = 400
        # 窗口宽高为100
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.master.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
        #############

        Label(self.master,text="\n一，本软件采用python编写，github地址：https://github.com/mapyJJJ/100-\n\n二,软件接口均来源于网络，用户可自由更换, 也可通过设置页面一键从网络获取\n\n三，部分剧集地址获取较慢，并非卡死，是由于网站反爬造成，请耐心等待几秒即可\n\n四，请在使用前软件检测环境是否齐全\n\n五，软件无需安装，请保存文件加内的其他配置文件，不要擅自修改或删除！",font=('宋体',13)).pack(side=TOP)
class check():
    def __init__(self):
        self.master=Toplevel()
        self.master.title('使用说明')

        self.jiekou_one=StringVar()
        self.jiekou_two=StringVar()
        self.jiekou_three=StringVar()
        self.jiekou_four=StringVar()

        #############
        sw = self.master.winfo_screenwidth()
        # 得到屏幕宽度
        sh = self.master.winfo_screenheight()
        # 得到屏幕高度
        ww = 650
        wh = 500
        # 窗口宽高为100
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.master.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
        #############
        Label(self.master,text="\n一，浏览器检测，确保您的电脑有谷歌浏览器，并设为默认\n\n二,下载安装对应版本的chromedriver驱动器，放置谷歌浏览器的安装录目即可",font=('宋体',13)).pack(side=TOP)
