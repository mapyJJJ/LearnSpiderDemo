import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}
url="http://maoyan.com/board/4?offset={offset}"
def get_movie_parse():
    x = PrettyTable(['电影名', '主演', '上映时间', '评分'])
    for i in range(0,91,10):
        all_name, all_star, all_time, all_score = [], [], [], []
        page_url=url.format(offset=str(i))
        req=requests.get(url=page_url,headers=headers)
        soup=BeautifulSoup(req.text,'lxml')
        name=soup.select('.movie-item-info .name a')
        star=soup.select('.star')
        time=soup.select('.releasetime')
        score=soup.select('.score i')
        for j in range(0,10):
            all_name.append(name[j].text)
            all_star.append("".join(star[j].text).split()[0])
            all_time.append(time[j].text)
            all_score.append(score[2*j].text + score[2*j+1].text)
        for item in range(0,10):
            x.add_row([all_name[item],all_star[item],all_time[item],all_score[item]])
    return x
if __name__ == '__main__':
    x=get_movie_parse()
    print(x)