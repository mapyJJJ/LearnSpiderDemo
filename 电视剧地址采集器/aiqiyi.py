import random

import requests
from bs4 import BeautifulSoup

headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"}


def ai_page_parse(name):
    play_list=[]
    req = requests.get("https://so.iqiyi.com/so/q_{}?source=input&sr=238433250165".format(str(name)),
                       headers=headers)
    soup=BeautifulSoup(req.text,'lxml')
    details=soup.select(".result_info_link_more")
    for item in details:
        if "src=search" not in str(item.get('href')):  #排除其他结果
            pass
        else:
            play_list.append(item.get('href'))
    return play_list,soup

def ai_video_list(choose_num,play_list):
    all_url = []
    if str(choose_num) == "1":
        index=0
        finally_video_url = play_list[0]
        req=requests.get(finally_video_url,headers=headers)
        soup=BeautifulSoup(req.text,'lxml')
        moive_title=soup.select(".info-intro-title")
        star = soup.select(".episodeIntro-director a")
        time_count=soup.select(".episodeIntro-time")
        all_url_list=soup.select(".numlist-wrapper ul li a")
        title_num=[]
        for li in all_url_list:
            if li.get('title') in title_num:
                break
            else:
                all_url.append(li.get('href'))
                title_num.append(li.get('title'))
    elif str(choose_num) == '2':
        index = random.randint(0, len(play_list)) - 1
        finally_video_url = play_list[index]
        req = requests.get(finally_video_url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        moive_title = soup.select(".info-intro-title")
        star = soup.select(".episodeIntro-director a")
        time_count = soup.select(".episodeIntro-time")
        all_url_list = soup.select(".numlist-wrapper ul li a")
        title_num = []
        for li in all_url_list:
            if li.get('title') in title_num:
                break
            else:
                all_url.append(li.get('href'))
                title_num.append(li.get('title'))
    return all_url,index,moive_title,star,time_count,finally_video_url
