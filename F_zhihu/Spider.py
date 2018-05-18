from F_zhihu.Parser import Json
from F_zhihu.Https import Http
from F_zhihu import Setting
from multiprocessing import Pool
import random,time,redis
from Z_getProxy import getProxy

class Spider(Http):
    def AFCODE(self):
        while True:


    def PMCODE(self):
        pass

    def completed(self, symbol):
        # 检测爬虫是否完成
        if r.scard(symbol) == 0:
            time.sleep(20)
            if r.scard(symbol) == 0:
                print('爬虫已结束')
                return True

    def proxyCount(self,processID):
        #检测代理的剩余量,补充及大休眠
        if r.scard('proxy') < 30:
            getProxy.getProxy()

    def randomUrl(self,symbol,page):
        token=r.spop('newID')
        url = Setting.url[symbol].format(id=token, page=page)
        return token,url

    def requestsIt(self,url):
        proxy = r.srandmember('proxy')
        htmlCode=self.get(url,
                      headers={'User-Agent':random.choice(Setting.UA),'Cookie':random.choice(Setting.Cookies)},
                      proxies={'proxy':proxy})
        return htmlCode


    def allFollowing(self,page):
        #获取所有关注者及子孙关注着token
        url = Setting.url['newID'].format(id=token, page=page)
        proxy = r.srandmember('proxy')
        htmlCode=self.get(url,
                          headers={'User-Agent': random.choice(Setting.UA),'Cookie': random.choice(Setting.Cookies)},
                          proxies={'proxy': proxy})
        while True:
            following=Json(htmlCode)
            if following.isEnd() == True:
                # 末页,最终解析
                followList = following.parseFollow()
                for newToken in followList:
                    r.sadd('newID', newToken)
                r.sadd('oldID', token)

    def parseMessage(self):
        #解析所有获取过的token信息
        token=r.spop('oldID')
        url = Setting.url['oldID'].format(token=token)
        proxy =r.srandmember('proxy')
        htmlCode=self.get(url,
                          headers={'User-Agent': random.choice(Setting.UA),
                                   'Cookie': random.choice(Setting.Cookies)},
                          proxies={'proxy':proxy})
        message=Json(htmlCode)

def main(processID):
    '''
    运行总步骤
    :param processID:编号--Just For Test
    '''
    while True:
        page=0
        spider.completed('newID')
        spider.proxyCount(processID)
        token,url=spider.randomUrl('newID',page)
        htmlCode=spider.requestsIt(url)
        if htmlCode==None:
            r.sadd('oldID',token)
            r.srem('proxy',proxy)
    # spider.AFCODE()#爬取所有人的token
    time.sleep(100)
    spider.PMCODE()#根据token爬取所有信息

if __name__=='__main__':
    #链接到redis库
    pool=redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)
    r=redis.Redis(connection_pool=pool)

    #定义spider类
    spider=Spider()

    #开启15个进程爬爬爬
    p=Pool(15)
    for i in range(15):
        time.sleep(i)
        p.apply_async(main,args=(i,))
    p.close()
    p.join()
