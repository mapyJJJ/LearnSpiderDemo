#选择剧集 顶级窗口１
#
from tkinter import *
import tkinter.messagebox as msgbox
from play_video import play

class select_play():
    def __init__(self,url_list,jiekou_num,name):
        self.name = name
        self.url_list=url_list
        self.master_one = Toplevel()
        self.master_one.title("＜"+self.name+">"+"选集播放")
        self.jiekou_num=jiekou_num
        ######################
        sw = self.master_one.winfo_screenwidth()
        # 得到屏幕宽度
        sh = self.master_one.winfo_screenheight()
        # 得到屏幕高度
        ww = 500
        wh = 500
        # 窗口宽高为100
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.master_one.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
        ######################
        self.play_num = IntVar()
        self.play_num.set(1)
        Label(self.master_one,text="如果需要切换线路，请关闭本窗口，切换线路后再次打开！！！").pack()
        farme_one=Frame(self.master_one)
        farme_two=Frame(self.master_one)
        farme_three=Frame(self.master_one)
        farme_four=Frame(self.master_one)
        farme_five=Frame(self.master_one)
        farme_six=Frame(self.master_one)
        for num, url in enumerate(self.url_list[:-1]):
            number=num+1
            if number <= 18:
                Radiobutton(farme_one, text="第%s集" % str(number), variable=self.play_num, value=number,
                        command=self.select_to_play).pack()
            elif number > 18 and number <= 36:
                Radiobutton(farme_two, text="第%s集" % str(number), variable=self.play_num, value=number,
                            command=self.select_to_play).pack()
            elif number > 36 and number <= 54:
                Radiobutton(farme_three, text="第%s集" % str(number), variable=self.play_num, value=number,
                            command=self.select_to_play).pack()
            elif number > 54 and number <= 72:
                Radiobutton(farme_four, text="第%s集" % str(number), variable=self.play_num, value=number,
                            command=self.select_to_play).pack()
            elif number >72 and number <=90:
                Radiobutton(farme_five, text="第%s集" % str(number), variable=self.play_num, value=number,
                            command=self.select_to_play).pack()
            else:
                Radiobutton(farme_six, text="第%s集" % str(number), variable=self.play_num, value=number,
                            command=self.select_to_play).pack()
        farme_one.pack(side=LEFT)
        farme_two.pack(side=LEFT)
        farme_three.pack(side=LEFT)
        farme_four.pack(side=LEFT)
        farme_five.pack(side=LEFT)
        farme_six.pack(side=LEFT)
        self.master_one.mainloop()
    def select_to_play(self):
        num = self.play_num.get()
        a=msgbox.askokcancel("确定","播放第%s集" % str(num),parent=self.master_one)
        if a == True:
            play(self.url_list,num,self.jiekou_num)
        else:
            pass
