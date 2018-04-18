import time,requests
from bs4 import BeautifulSoup

def getProxy(page):
    print('***********************************************')
    print('开始获取代理IP:')
    list=requestIP(page)
    proxiesList=testIP(list)
    return proxiesList

def requestIP(num):
    '''
    从高匿网站获取IP，并生成文档
    '''
    IPlist=[]
    api='http://www.xicidaili.com/nn/{}'
    header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    for i in range(1,num+1):
        url=api.format(i)
        res=requests.get(url,headers=header)
        soup=BeautifulSoup(res.text,'lxml')
        container=soup.find_all(name='tr')[1:]
        for i in container:
            ip=i.find_all('td')[1].text
            port=i.find_all('td')[2].text
            IPlist.append('http://'+ip+':'+port)
        time.sleep(1)
    return IPlist

def testIP(list):
    '''
    测试爬取的ip是否可用
    '''
    url='http://www.baidu.com'
    n=1
    for i in list:
        proxy={'proxy':i}
        try:
            res=requests.get(url,proxies=proxy)
            res.raise_for_status()
            print('第{}个ip：{} 成功'.format(n, i))
        except requests.exceptions.RequestException as e:
            list.remove(i)
            print('***********************************************')
            print('ip:{}异常:{}'.format(i,e))
        n+=1
    print('代理IP检测完毕')
    print('***********************************************')
    return list