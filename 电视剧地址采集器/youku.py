import random
from time import sleep
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import re
from selenium import webdriver

headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"}

def page_parse(name):
    play_list=[]
    data={"name_encode":str(name)}
    url_encode=urlencode(data)
    name=re.findall('=(.*)', url_encode)
    url="https://so.youku.com/search_video/q_{}".format(name[0])
    browser=webdriver.PhantomJS()
    browser.get(url)
    sleep(0.1)
    soup=BeautifulSoup(browser.page_source,'lxml')
    item=soup.select('.row-ellipsis .row-end')
    for i in item:
        play_list.append(i.get('href'))
    return play_list,soup

def video_list(choose_num,play_list):
    all_url = []
    if str(choose_num) == "1":
        index=0
        finally_video_url = play_list[0]
        browser = webdriver.PhantomJS()
        browser.get(play_list[0])
        sleep(0.1)
        page_soup=BeautifulSoup(browser.page_source,'lxml')
        moive_title=page_soup.select('.p-row')
        star=page_soup.select('.p-performer a')
        time_count=page_soup.select('.pub')
        url_list=page_soup.select(".p-drama-grid li")
        for url in url_list:
            if "preview" in str(url):    #排除预告集
                pass
            else:
                play_list=url.select('a')
                all_url.append('http:'+play_list[0].get('href'))
        print('剧集'+str(all_url))
    elif str(choose_num) == '2':
        index = random.randint(0, len(play_list)) - 1
        browser = webdriver.PhantomJS()
        finally_video_url = play_list[index]
        browser.get(play_list[index])
        sleep(0.1)
        page_soup = BeautifulSoup(browser.page_source, 'lxml')
        moive_title = page_soup.select('.p-row')
        star = page_soup.select('.p-performer a')
        time_count = page_soup.select('.pub')
        url_list = page_soup.select(".p-drama-grid li")
        for url in url_list:
            if "preview" in str(url):  # 排除预告集
                pass
            else:
                play_list = url.select('a')
                all_url.append('http:' + play_list[0].get('href'))
    return all_url,index,moive_title,star,time_count,finally_video_url