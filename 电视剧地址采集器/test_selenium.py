from time import *
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display

#尝试自动化解决集数过多的剧集
def selenium_parse(finally_video_url):
    #browser=webdriver.PhantomJS()
    #尝试使用chromedriver驱动（需要用户自己安装）
    try:
        #无窗口的selenium自动化获取
        opt = webdriver.ChromeOptions()
        opt.set_headless()
        browser=webdriver.Chrome(options=opt)
    except:  #适用于在linux下的自动化获取
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")  #linux 下需要使用--no-sandbox 选项来调用chrome
        browser=webdriver.Chrome(chrome_options=options) 
    browser.get(finally_video_url)  #打开剧集详情页面
    browser.find_element_by_link_text("全部").click()  #点击全部按钮，展示每一集的链接
    sleep(0.5)
    soup=BeautifulSoup(browser.page_source,'lxml')
    url=[]
    all_list=soup.select("._playsrc_series .mod_episode .item a")
    for item in all_list:
        url.append(item.get('href'))
    url.reverse()
    find_site=url.index("javascript:;")
    reverse_url_list=url[0:int(find_site)]
    reverse_url_list.reverse()
    reverse_url_list.insert(0,"[+]成功获取到完整地址")
    browser.quit()  #退出selenium虚拟浏览器
    return reverse_url_list  #返回我们获取到的完整的链接