from time import *
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display

#尝试自动化解决集数过多的剧集
def selenium_parse(finally_video_url):
    display = Display(visible=0, size=(800, 600))
    display.start()
    #browser=webdriver.PhantomJS()
    #尝试使用chromedriver驱动（需要用户自己安装）
    try:
        browser=webdriver.Chrome()
    except:
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        browser=webdriver.Chrome(chrome_options=options)
    browser.get(finally_video_url)
    browser.find_element_by_link_text("全部").click()
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
    browser.quit()
    display.stop()
    return reverse_url_list