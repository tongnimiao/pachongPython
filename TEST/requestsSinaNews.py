import requests
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool
import json
import re
import pandas
import os,time
import threading

news_total=[]
def getNewsDetail(newsUrl):
    result={}
    res = requests.get(newsUrl)
    res.encoding='utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    result['title']=soup.select('.main-title')[0].text
    result['newsSource']=soup.select('.source')[0].text
    dt = datetime.strptime(soup.select('.date-source')[0].contents[1].text, '%Y年%m月%d日 %H:%M')
    result['data']=dt.strftime('%Y-%m-%d')
    result['article']=' '.join([i.text.strip() for i in soup.select('#article p')[1:-1]])
    result['editor']=(re.compile('((责任编辑：)|(作者:))').sub('',soup.select('.show_author')[0].text)).strip(' ')
    result['commit']=soup.select('.num')[0].text
    result['keyword']=soup.select('#article-bottom a')[0]
    news_total.append(result)
    print(result)

def parseListLinks(url):
    newsdetails=[]
    res=requests.get(url)
    jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
    for i in jd['result']['data']:
        newsdetails.append(getNewsDetail(i['url']))
    return newsdetails

def pagenews(*args):
    url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}'
    if len(args)==2:
        if not isinstance(args[0],int) or not isinstance(args[1],int) or args[0] >= 499 or args[0] <= 0 or args[1] >= 499 or args[1] <= 0:
            print('checkNumber')
        elif args[0]>args[1]:
            print("checkTuple")
        else:
            for i in range(args[0],args[1]+1):
                newsurl=url.format(i)
                parseListLinks(newsurl)
    elif len(args)==1:
        if not isinstance(args[0],int) or args[0] >= 499 or args[0] <= 0:
            print("checkNumber")
        else:
            newsurl=url.format(args[0])
            parseListLinks(newsurl)
    else:
        print('checkTupleNumber')

# start=time.time()
# pagenews(1,3)
# end=time.time()
# print(end-start)

# if __name__=='__main__':
#     start=time.time()
#     p=Pool(4)
#     p.apply_async(pagenews,args=(1,3))
#     p.close()
#     p.join()
#     end=time.time()
#     print(end-start)

start=time.time()


# for i in range(5):
#     pagenews(i+1)

pool = Pool(4) #建立进程池
pool.map(pagenews, (i+1 for i in range(5)))#映射到主函数中进行循环

# t=[threading.Thread(target=pagenews,args=(page+1,)) for page in range(5)]
# for a in t:
#     a.start()
# for b in t:
#     b.join()


end=time.time()
print(end-start)