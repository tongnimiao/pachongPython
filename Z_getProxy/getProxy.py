import time,requests,redis,random
from bs4 import BeautifulSoup
from Z_getProxy import setting

def getProxy():
    print('***********************************************')
    print('开始获取代理IP:')
    '''
    从xicidaili.com获取高匿IP
    '''

    pool=redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)
    r=redis.Redis(connection_pool=pool)

    IPlist=[]
    api='http://www.xicidaili.com/nn/{}'
    url=api.format(1)
    if r.scard('proxy')==0:
        res=requests.get(url,headers={'User-Agent':random.choice(setting.UA)})
    else:
        pro=r.srandmember('proxy')
        res=requests.get(url,headers={'User-Agent':random.choice(setting.UA)},proxies={'proxy':pro})
    soup=BeautifulSoup(res.text,'lxml')
    container=soup.find_all(name='tr')[1:]
    for i in container:
        ip=i.find_all('td')[1].text
        port=i.find_all('td')[2].text
        IPlist.append('http://'+ip+':'+port)
    '''
    测试IP
    '''

    testUrl='http://www.baidu.com'
    n=1
    for ip in IPlist:
        proxy={'proxy':ip}
        try:
            res=requests.get(testUrl,headers={'User-Agent':random.choice(setting.UA)},proxies=proxy)
            res.raise_for_status()
            r.sadd('proxy',ip)
            print('第{}个ip：{} 成功'.format(n, ip))
        except requests.exceptions.RequestException as e:
            print('***********************************************')
            print('ip:{}异常:{}'.format(ip,e))
        n+=1
    print('代理IP检测完毕')

if __name__=='__main__':
    getProxy()