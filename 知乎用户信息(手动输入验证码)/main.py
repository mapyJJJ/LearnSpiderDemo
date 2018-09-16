#!/usr/bin/python3
#
#   获取知乎某一用户的关注列表和粉丝列表的详细信息
#   直接运行该脚本即可
#   验证码为手动输入,当访问受阻后会自动弹出页面输入验证码
#   author:mapyJJJ
#
import json
import pymongo
import requests
from Change_headers import get_headers
from zhihu_Verification import login_page

#关注列表模版
guanzhu_url="https://www.zhihu.com/api/v4/members/{user_name}/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset={offset}&limit=20"

#粉丝列表模版
fans_url="https://www.zhihu.com/api/v4/members/{user_name}/followers?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset={offset}&limit=20"


def control_spider(g_url,page):
    page+=1
    g_req=requests.get(g_url,headers=get_headers()[0])
    try:
        if json.loads(g_req.text)['paging']['is_end'] == False:
            parse_guanzhu_fans(g_req)
            next_url=json.loads(g_req.text)['paging']['next']
            print('关注列表当前页数:%s' % str(page))
            return control_spider(next_url,page=page)
        else:
            parse_guanzhu_fans(g_req)
            print('这是最后一页')
            print('当前页数:%s' % str(page))
    except Exception as msg:
        print('出错,ip需要验证 无法获取键值:%s' % msg)
        print('跳转到手动验证页面')
        login_test_img_url=json.loads(g_req.text)['error']['redirect']
        login_page(url=login_test_img_url)
def parse_guanzhu_fans(g_req):
    data=json.loads(g_req.text)['data']
    for item in data:
        user_data = {
            'name': '',  # 昵称
            'type': '',  # 类型
            'headline': '',  # 简介
            'answer_count': '',  # 回答数
            'avatar_url': '',  # 头像链接
            'index_url': '',  # 用户主页
        }
        for key in user_data.keys():
            if key=='index_url':
                index_url = "https://www.zhihu.com/people/%s" % item['url_token']
                user_data['index_url']=index_url
            else:
                user_data[key]=item[key]
        save_to_mongo(user_data)


def save_to_mongo(user_data):
    client=pymongo.MongoClient('localhost',27017)
    db=client['zhihu_user']
    user=db[user_name]
    user.insert_one(dict(user_data))

if __name__ == '__main__':
    # first url
    user_name = input('输入用户的url_token:')
    g_url = guanzhu_url.format(user_name=user_name, offset=0)
    f_url = fans_url.format(user_name=user_name, offset=0)
    page = 0
    control_spider(g_url=g_url,page=page)
    control_spider(g_url=f_url,page=page)
