import random
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
from youku import *
from aiqiyi import *
#爬虫
#问题:腾讯视频每一集列表,若集数太多.会将列表折叠起来,尝试通过破解js文本来获取参数加密方式,但其过于复杂,目前没有实现,依然采用webdriver方法
#
#


headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}
def aiqiyi(name,choose_num):
    title="爱奇艺视频来源:"
    play_list,soup=ai_page_parse(name)
    all_url, index, moive_title, star, time_count, finally_video_url=ai_video_list(choose_num,play_list)
    aiqiyi_details(name,soup,index)
    return all_url,title,moive_title,star,time_count,finally_video_url

def youku(name,choose_num):
    title="优酷视频来源:"
    play_list,soup=page_parse(name)
    print('!!!'+str(play_list))
    all_url, index, moive_title, star, time_count, finally_video_url=video_list(choose_num,play_list)
    youku_details(name, soup, index)
    return all_url,title,moive_title,star,time_count,finally_video_url

def tenxun(name,choose_num):   #腾讯视频链接获取
    moive_title, star, time_count=[],[],[]
    title="腾讯视频来源:"
    all_url,video_url=[],[]
    url = "https://v.qq.com/x/search/?q={}".format(str(name))
    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    result_title = soup.select('.result_title a')
    for item in result_title:
        if 'detail' in str(item):
            video_url.append(item.get('href'))  #获取完所有的符合要求的剧集url,排除单个视频
    #print(video_url)
    if len(video_url) != 0:   #判断是否获得了结果
        if str(choose_num) == '1':  #当用户选择 只取第一个时
            index=0
            #需要返回页面url,以便纠错
            finally_video_url=video_url[0]
            req=requests.get(url=video_url[0],headers=headers)
            soup_page=BeautifulSoup(req.text,'lxml')
            moive_title=soup_page.select('.video_title_cn a')
            star=soup_page.select('.video_actor .name')
            time_count=soup_page.select('.video_type .type_item .type_txt')
            play_list=soup_page.select('.mod_episode .item a')  #定位到每一集的链接
            for each_play in play_list:
                if '预告' in str(each_play):  #排除预告集
                    pass
                else:
                    all_url.append(each_play.get('href'))
        elif str(choose_num) == '2':  #随机挑选一个
            index=random.randint(0,len(video_url))-1
            finally_video_url=video_url[index]
            req=requests.get(url=video_url[index],headers=headers)
            soup_page = BeautifulSoup(req.text, 'lxml')
            #获取剧名 演员列表 简介
            moive_title=soup_page.select('.video_title_cn a')
            star=soup_page.select('.video_actor .name')
            time_count=soup_page.select('.type_item .type_txt')
            play_list = soup_page.select('.mod_episode .item a')  # 定位到每一集的链接
            for each_play in play_list:
                if '预告' in str(each_play):  # 排除预告集
                    pass
                else:
                    all_url.append(each_play.get('href'))
        tenxun_details(name,soup,index)
    else:
        all_url.append('没有查找到您需要的剧集')
    #print(all_url)
    return all_url,title,moive_title,star,time_count,finally_video_url


#######此处爬取封面等信息#########
def tenxun_details(name,soup,index):  #获取相关剧集的图片简介等
    image_url=[]
    each_result=soup.select('._infos')
    for item in each_result:
        if 'detail' in str(item):
            pic_item=item.select('.figure img')
            image_url.append('http:'+pic_item[0].get('src'))
    urlretrieve(image_url[index],'download.png')
def youku_details(name,soup,index):
    image_url = []
    each_result=soup.select('.sk-mod')
    for item in each_result:
        if "row-ellipsis" in str(item):
            pic_item=item.select('.pack-cover img')
            image_url.append('http:'+pic_item[0].get('src'))
    urlretrieve(image_url[index],'download.png')
def aiqiyi_details(name,soup,index):
    image_url = []
    imglist = soup.select('.figure img')
    for i in imglist:
        if 'vip' not in str(i.get('src')):
            image_url.append('http:' + i.get('src'))
        else:
            pass
    urlretrieve(image_url[index],'download.png')
#################


def n_to_u(name,choose_num,choose_source_num):
    print(choose_source_num)
    if name == "":
        raise TypeError
    else:
        if choose_source_num == 2:
            return tenxun(name,choose_num)
        elif choose_source_num == 3:
            return youku(name,choose_num)
        elif choose_source_num == 1:
            return aiqiyi(name,choose_num)

