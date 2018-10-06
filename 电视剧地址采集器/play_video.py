#打开浏览器播放
import webbrowser
import json

def to_play(url,jiekou_num):
    with open("jiekou.json", 'r') as load_f:
        jiekou_url_list = json.load(load_f)
    url = jiekou_url_list['jiekou'][str(jiekou_num)] + url
    webbrowser.open(url)

def play(url_list,num,jiekou_num):
    with open("jiekou.json", 'r') as load_f:
        jiekou_url_list = json.load(load_f)
    url=jiekou_url_list['jiekou'][str(jiekou_num)]+url_list[num-1]
    webbrowser.open(url)