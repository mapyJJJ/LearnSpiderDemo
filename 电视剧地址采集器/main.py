#!/usr/bin/python3
import webbrowser

import PIL.Image
from PIL import ImageTk
from tkinter import *
import tkinter.messagebox as msgbox
from name_to_url import n_to_u
from toplevel_one import select_play
from test_selenium import selenium_parse
from play_video import to_play
from toplevel_setting import setting
from menubar import *
#1,从各大影视网站获取相应视频的链接
#2,获取免费的vip接口
#主窗口

class Video_APP():
    def __init__(self):
        self.title="vip视频在线观看"
        self.author="金牛小子"
        self.version='V1.0'
        self.finally_video_url=''
        self.root=Tk(className=self.title)
        self.menubar=Menu(self.root)
        self.root.resizable(0, 0)

        self.moive_title=StringVar()
        self.moive_star=StringVar()
        self.t_c_item=StringVar()

        self.menubar.add_command(label="使用必看",command=gui_info)
        self.menubar.add_command(label="环境配置", command=check)
        self.root.config(menu=self.menubar)

        self.farme_left=Frame(self.root)
        #左边框架
        #左上图片展示
        im=PIL.Image.open("download.png")
        self.photo=ImageTk.PhotoImage(im)
        self.photolable=Label(self.farme_left,image=self.photo)
        self.photolable.pack(padx=2,pady=0)
        #图片下面的详情页介绍  简介需限制长度
        self.text_label1=Label(self.farme_left,text=self.moive_title,font=("宋体",20),width=26,wraplength=300)
        self.text_label1.pack(anchor=N)
        self.text_label2=Label(self.farme_left,text=self.moive_star,justify=CENTER,font=("宋体",15),width=26,wraplength=300)
        self.text_label2.pack(anchor=N)
        self.text_label3=Label(self.farme_left,text=self.t_c_item,justify=CENTER,font=("宋体",15),width=26,wraplength=300)
        self.text_label3.pack(anchor=N)
        self.farme_left.pack(side=LEFT,padx=0)
        #########################################

        farme_right = Frame(self.root)
        # 右边框架

        farme_right_one=Frame(farme_right)
        Label(farme_right_one,text="选择线路:",font=("宋体",13),fg="green").pack(side=LEFT,anchor=NW,padx=10,pady=10)
        ROAD = [("线路一", 1), ("线路二", 2), ("线路三", 3), ("线路四", 4)]
        self.v,self.w,self.x,self.t= IntVar(),IntVar(),IntVar(),IntVar()
        self.v.set(1)
        for lang, num in ROAD:
            Radiobutton(farme_right_one, text=lang, variable=self.v, value=num,font=("宋体",12)).pack(pady=10,padx=10,side=LEFT)
        farme_right_one.pack(side=TOP)

        farme_right_two=Frame(farme_right)
        Label(farme_right_two,text="输入视频网址:",fg="green",font=("宋体",13)).pack(anchor=NW,side=LEFT,padx=7,pady=20)
        self.website_url=StringVar()
        Entry(farme_right_two,textvariable=self.website_url,width=40).pack(side=LEFT,padx=7,pady=20)
        Button(farme_right_two, text="开始播放",command=self.play).pack(side=LEFT,padx=7,pady=20)
        farme_right_two.pack(side=TOP)

        farme_right_three=Frame(farme_right)
        Label(farme_right_three,text="播放来源:",fg="green",font=("楷书",13)).pack(padx=10,pady=10,anchor=NW,side=LEFT)
        self.w.set(2)
        website=[("爱奇艺",1),("腾讯视频",2),("优酷视频",3),("芒果TV",4)]
        for lang, num in website:
            Radiobutton(farme_right_three, text=lang, variable=self.w, value=num,font=("宋体",12),command=self.choose_source).pack(padx=5,pady=0,side=LEFT)
        farme_right_three.pack(side=TOP)

        farme_right_five = Frame(farme_right)
        self.video_name=StringVar()
        Label(farme_right_five, text="剧集名称:", fg="green", font=("宋体", 12)).pack(anchor=NW,side=LEFT,padx=17,pady=10)
        Entry(farme_right_five, textvariable=self.video_name, width=40).pack(side=LEFT,padx=17,pady=10)
        Button(farme_right_five, text="自动获取",command=self.spider_n_to_u).pack(side=RIGHT,padx=17,pady=10)
        farme_right_five.pack(side=TOP)

        farme_right_type=Frame(farme_right)
        Label(farme_right_type,text="视频类型设置:",fg="green").pack(side=LEFT,padx=0)
        self.t.set(1)
        site_choose=[("电视剧",1),('电影',2)]
        for choose,choose_num in site_choose:
            Radiobutton(farme_right_type,text=choose,variable=self.t,value=choose_num,font=("宋体",10),command=self.choose_btn).pack(side=LEFT,padx=0)
        farme_right_type.pack(side=TOP)

        farme_right_choose=Frame(farme_right)
        Label(farme_right_choose,text="剧集地址设置:",fg="green").pack(side=LEFT,padx=0)
        self.x.set(1)
        site_choose=[("默认选择一个匹配结果",1),('随机匹配',2)]
        for choose,choose_num in site_choose:
            Radiobutton(farme_right_choose,text=choose,variable=self.x,value=choose_num,font=("宋体",10),command=self.choose_btn).pack(side=LEFT,padx=0)
        farme_right_choose.pack(side=TOP)

        farme_right_four=Frame(farme_right)
        sb=Scrollbar(farme_right_four)
        sb.pack(side=RIGHT,fill=Y)
        self.lb=Listbox(farme_right_four,yscrollcommand=sb.set,width=40,height=13)
        self.lb.insert(END,"准备就绪!")
        self.lb.pack(side=LEFT,fill=BOTH)
        sb.config(command=self.lb.yview)
        farme_right_four.pack(side=LEFT,padx=17,pady=10)

        farme_right_six=Frame(farme_right)
        Button(farme_right_six,text="导入播放列表",height=1,command=self.add_result_play).pack(side=TOP)
        Button(farme_right_six, text="一键快速播放", height=1, command=self.start_to_play).pack(side=TOP)
        sb = Scrollbar(farme_right_six)
        sb.pack(side=RIGHT, fill=Y)
        self.lb1 = Listbox(farme_right_six, yscrollcommand=sb.set,height=5)
        self.lb1.insert(END, "等待导入")
        self.lb1.pack(side=LEFT, fill=BOTH)
        sb.config(command=self.lb1.yview)
        farme_right_six.pack(pady=0)

        farme_right_seven=Frame(farme_right)
        Button(farme_right_seven, text="联系作者",width=20,command=self.contact_me).pack(side=TOP)
        Button(farme_right_seven, text="系统设置",width=20,command=setting).pack(side=TOP)
        Label(farme_right_seven, text="by金牛小子 V1.1").pack(side=TOP)
        farme_right_seven.pack(padx=20,pady=0)
        #结束
        farme_right.pack()

        mainloop()
    def contact_me(self):
        webbrowser.open("https://github.com/mapyJJJ/100-")

    def spider_n_to_u(self):
        choose_num=self.choose_btn()   #获取用户选择(匹配第一个或是随机)
        self.name=self.video_name.get()     #获取用户输入的名称
        choose_source_num=self.choose_source()
        try:
            if choose_source_num == 4:
                msgbox.showerror('抱歉','我们不建议使用傻逼芒果台，其电视剧综艺节目内容过于弱智，长期观看会有损智力，为了您的健康着想，作者思索再三决定不开发芒果台的链接获取功能')
            else:
                all_url_tx,title,moive_title,star,time_count,finally_video_url=n_to_u(self.name,choose_num,choose_source_num)
            self.finally_video_url=finally_video_url
            print(len(all_url_tx))
            self.lb.delete(0,END)     #清空滚动框
            self.lb.insert(END, title)
            for number,item in enumerate(all_url_tx):
                self.lb.insert(END,str(item))
            #刷新图片
            self.photo=ImageTk.PhotoImage(PIL.Image.open("download.png"))
            self.photolable.config(image=self.photo)
            #刷新文字信息
            start_name_string,t_c_item_string="",""
            self.moive_title=moive_title[0].text
            self.text_label1.config(text=self.moive_title,width=26)
            for star_name in star:
                start_name_string+=star_name.text+","
            self.text_label2.config(text=start_name_string,width=26)
            try:
                t_c_item_string+=time_count[0].text+"\n"
                self.text_label3.config(text=t_c_item_string,width=26)
            except:
                pass
        except TypeError:
            print("输入为空")
            msgbox.showerror('错误','您没有输入或者输入有误!!!\n 请重新输入或者更换来源再次查询！！！')
    def add_result_play(self):
        result_list=self.lb.get(0,END)
        if len(result_list) == 1:
            msgbox.showerror("错误",'请您先输入剧集名称，然后点击［自动获取］按钮后再进行导入操作！！')
        # 当链接中出现js动态脚本时，进行处理
        elif "javascript" in str(result_list):
            msgbox.showerror("提示",'因剧集过多，地址获取不完整，请等待几秒，为您修复地址')
            self.lb.delete(0, END)
            try:
                reverse_url_list=selenium_parse(self.finally_video_url)
                self.lb.delete(0, END)
                for url in reverse_url_list:
                    self.lb.insert(END, str(url))
                msgbox.showerror("成功", '成功获取到完整地址！')
            except:
                msgbox.showerror("失败", '获取失败，请您手动输入地址！！')
        else:
            video_url_list=result_list[1:]
            self.lb1.delete(0,END)
            for url in video_url_list:
                self.lb1.insert(END,str(url))
            self.lb1.insert(END,"一共获取到%s集" % str(len(video_url_list)))
    def play(self):
        url=self.website_url.get()
        try:
            re.match("",url)
            msgbox.showerror("错误", "没有输入地址")
        except:
            to_play(url,self.v.get())

    ########################
    def choose_btn(self):
        choose_num = self.x.get()
        return choose_num
    def choose_source(self):
        choose_source_num=self.w.get()
        return  choose_source_num
    def start_to_play(self):
        url_list = self.lb1.get(0, END)
        jiekou_num=self.v.get()
        select_play(url_list,jiekou_num,self.name)
    ########################


if __name__ == '__main__':
    app=Video_APP()
