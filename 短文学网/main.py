# -*- coding:utf-8 -*-
from passage_spider import Spider

def get_url():
    with open('url.txt','r') as f:
        url_list=f.readlines()
    return url_list

if __name__ == '__main__':
    url_list=get_url()
    Spider(url_list=url_list).spy()


