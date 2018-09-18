import os
import requests
import urllib.request
import json
import re
from bs4 import BeautifulSoup
headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}

def download_pic(url):
    global pic_count
    pic_count+=1
    try:
        path = "/root/{}/{}.jpg".format(name, str(pic_count))
        print("[+]已下载:" + path)
        urllib.request.urlretrieve('http://' + url, filename=path)
    except:
        pass

def get_pic(pic_url):
    req=requests.get(pic_url,headers=headers)
    soup=BeautifulSoup(req.text,'lxml')
    json_parse=re.findall('gallery: JSON.parse(.*)', str(soup))
    try:
        json_url=re.findall('{.*}',json_parse[0])
        sub_image=json.dumps(json_url[0]).replace('\\','')
        img_url=re.findall('"http://(.*?)"',sub_image)
        for i in range(0,len(img_url),4):
            url=img_url[i]
            download_pic(url=url)
    except IndexError:
        print('坏的图片链接,自动跳过')

def get_pic_url():
    offset=0
    while True:   #循环构造url请求
        url = "https://www.toutiao.com/search_content/?offset={}&" \
              "format=json&keyword={}&autoload=true&count=20&cur_tab=1&from=search_tab".format(str(offset),name)
        req=requests.get(url)
        offset+=20
        req_data=json.loads(req.text)
        if req_data['return_count'] != 0:  #判断返回的数据是否为0
            print(req_data['return_count'])
            for item in req_data['data']:
                if 'has_gallery' in item.keys() and item['has_gallery']==True:  #判断文章的模式
                    get_pic(pic_url=item['article_url'])
                else:
                    print("本篇不是图片类型文章,自动跳过")
        else:
            print('爬取完毕')
            break


if __name__ == '__main__':
    pic_count=0
    name=input('输入查询图片的关键字(如街拍):')
    try:
        os.mkdir('/root/{}'.format(name))
    except:
        pass
    get_pic_url()