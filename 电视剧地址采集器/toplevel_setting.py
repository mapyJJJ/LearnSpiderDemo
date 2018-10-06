#设置窗口
import json
from tkinter import *
import tkinter.messagebox as msgbox
import requests
from bs4 import BeautifulSoup
headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}

class setting():
    def __init__(self):
        self.master=Toplevel()
        self.master.title('设置页面')

        self.jiekou_one=StringVar()
        self.jiekou_two=StringVar()
        self.jiekou_three=StringVar()
        self.jiekou_four=StringVar()

        #############
        sw = self.master.winfo_screenwidth()
        # 得到屏幕宽度
        sh = self.master.winfo_screenheight()
        # 得到屏幕高度
        ww = 450
        wh = 500
        # 窗口宽高为100
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.master.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
        #############

        ######接口设置#######
        farme_one=Frame(self.master)
        Label(farme_one,text="更新接口",font=('宋体',13)).pack(side=TOP)
        Label(farme_one, text="对应四个接口，若不更改，请留空", font=('宋体', 10)).pack(side=TOP)
        Entry(farme_one,textvariable=self.jiekou_one, width=40).pack(side=TOP,pady=5)
        Entry(farme_one,textvariable=self.jiekou_two, width=40).pack(side=TOP,pady=5)
        Entry(farme_one,textvariable=self.jiekou_three, width=40).pack(side=TOP,pady=5)
        Entry(farme_one,textvariable=self.jiekou_four, width=40).pack(side=TOP,pady=5)
        Button(farme_one,text="确定更新",command=self.change_jiekou).pack(side=RIGHT,pady=5)
        farme_one.pack(side=TOP)

        farme_two=Frame(self.master)
        Label(farme_two, text="批量获取解析接口", font=('宋体', 13)).pack(side=TOP)
        Label(farme_two, text="默认从小米解析网站获取", width=40).pack(side=TOP, pady=5)
        Button(farme_two, text="开始", command=self.check_jiekou).pack(side=TOP, pady=5)
        farme_two.pack(side=TOP,pady=20)

    def change_jiekou(self):
        for num,value in enumerate([self.jiekou_one.get(),self.jiekou_two.get(),self.jiekou_three.get(),self.jiekou_four.get()]):
            jiekou_num=num+1
            if value == "":
                pass
                #print("接口%s为空！" % str(jiekou_num))
            else:
                with open('jiekou.json','r') as load_f:
                    jiekou_url_list=json.load(load_f)
                    jiekou_url_list['jiekou'][str(jiekou_num)]=str(value)
                load_f.close()
                with open('jiekou.json','w') as load_f:
                    load_f.write(json.dumps(jiekou_url_list))
                load_f.close()
    def check_jiekou(self):
        req=requests.get("http://jiekou.xiaomil.com/",headers=headers)
        soup=BeautifulSoup(req.text,'lxml')
        url_list=soup.select("xiaomil_ul form div lib_3 a")
        for url in url_list:
            print(url.get('href'))


if __name__ == '__main__':
    app=setting()