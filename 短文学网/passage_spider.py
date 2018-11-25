import requests
from bs4 import BeautifulSoup
import pymongo
import threading

'''
    两种类型：1，文章形  (list-base-article)  需要进一步爬取
              2，句子（list-short-article）   
'''


class Spider:
    def __init__(self,url_list):
        self.url_list=url_list
        client=pymongo.MongoClient('localhost',27017)
        db=client['wenxue']
        self.passage=db['passage']
        self.article=db['article']

    def parse_page(self,url):  #处理页面请求（下载函数）
        try:
            req=requests.get(url=url)
            soup=BeautifulSoup(req.text,'lxml')
            return soup
        except:
            return None
    def short_article(self,url,start_num,end_num):   #短句子爬虫(起始url 第一个页面soup)
        for page in range(start_num,end_num):
            each_page_url=url.split('\n')[0]+'list_{}.html'.format(str(page))
            page_content=self.parse_page(each_page_url)
            short_list=page_content.select('.list-short-article ul li p a[target="_blank"]')
            for short in short_list:
                data={'short':short.text}
                self.passage.insert_one(data)
    def base_article(self,url,start_num,end_num):
        for page in range(start_num,end_num):
            each_page_url=url.split('\n')[0]+'list_{}.html'.format(str(page))
            page_content=self.parse_page(each_page_url)
            passage_list_url=page_content.select('.list-base-article ul li a[target="_blank"]')
            for passage_url in passage_list_url:
                article_url='https://www.duanwenxue.com'+passage_url['href']
                article_soup=self.parse_page(url=article_url)
                title=article_soup.select('h1')[0].text
                content=''
                for p in article_soup.select('.article-content p')[1:-5]:
                    content+='    '+p.text+'\n'
                data={
                    'title':title,
                    'article':content
                }
                self.article.insert_one(data)


    def spy(self):
        self.thread_one=[]
        self.thread_two=[]
        self.setNumber=int(input('线程数：'))
        for url in self.url_list:
            soup=self.parse_page(url)
            if soup == None:
                pass
            else:
                self.all_page_num=(str(soup.select('.pinfo')[0]).split('</span>/')[1].split('</strong>'))[0]
                if soup.select('.list-base-article') != []:   #文章
                    start_num=1
                    for number in range(1,self.setNumber+1):
                        end_num=start_num+int(int(self.all_page_num)//self.setNumber)
                        if number == self.all_page_num:  #最后一个线程
                            t=threading.Thread(target=self.base_article,args=(url,start_num,self.all_page_num))
                            self.thread_one.append(t)
                        else:
                            t=threading.Thread(target=self.base_article,args=(url,start_num,end_num))
                            self.thread_one.append(t)
                        start_num=end_num
                    for t in self.thread_one:
                        t.start()
                    for t in self.thread_one:
                        t.join()

                if soup.select('.list-short-article') != []:  #短句
                    start_num=1
                    for number in range(1,self.setNumber+1):
                        end_num=start_num+int(int(self.all_page_num)//self.setNumber)
                        if number == self.all_page_num:  #最后一个线程
                            t=threading.Thread(target=self.short_article,args=(url,start_num,self.all_page_num))
                            self.thread_two.append(t)
                        else:
                            t=threading.Thread(target=self.short_article,args=(url,start_num,end_num))
                            self.thread_two.append(t)
                        start_num=end_num
                    for t in self.thread_two:
                        t.start()
                    for t in self.thread_two:
                        t.join()
                pass




