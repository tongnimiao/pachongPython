from F_zhihu.Parser import Json
from F_zhihu.Https import Http
from F_zhihu import Setting
from multiprocessing import Pool
import random,time,redis
from Z_getProxy import getProxy


def Spider(initID):
    r.sadd('newID',initID)

    #建立进程池
    p=Pool(15)
    for i in range(15):
        time.sleep(i)
        p.apply_async(allFollowID,args=(i,))#爬取所有关注者及子孙关注者ID
    p.close()
    p.join()

    #解析已爬token信息
    for i in range(15):
        time.sleep(i)
        p.apply_async(parseMessage,args=(i,))
    p.close()
    p.join()

def allFollowID(processID):
    '''
    爬取所有关注者及子孙关注者token
    :param processID: 进程编号,justForTest
    :return: None
    '''
    while True:
        #检测代理的剩余量,补充及大休眠
        if r.scard('proxy') < 10:
            if processID==0:
                getProxy.getProxy()
            time.sleep(100)
        proxy = r.srandmember('proxy')

        #检测爬虫是否完成
        if r.scard('newID')==0:
            time.sleep(20)
            if r.scard('newID')==0:
                break
            else:
                continue

        #从newID随机获取token并查询是否已解析
        A=r.spop('newID')
        if r.sismember('oldID',A):
            continue
        n=0#页码

        while True:
            followUrl=Setting.followUrl.format(id=A,page=n)
            htmlCode=httpClass.get(followUrl,
                                   headers={'User-Agent':random.choice(Setting.UA),'Cookie':random.choice(Setting.Cookies)},
                                   proxies={'proxy':proxy}
                                   )

            #访问失败跳过该token
            if htmlCode==None:
                r.sadd('oldID',A)
                r.srem('proxy',proxy)
                break


            parseClass = Json(htmlCode)
            if parseClass.isEnd() == True:
                #末页,最终解析
                followList=parseClass.parseFollow()
                for i in followList:
                    r.sadd('newID',i)
                r.sadd('oldID',A)

                momentTime=time.time()
                time.sleep(3)
                print('已爬%s条,未爬%s条'%(r.scard('oldID'),r.scard('newID')))
                print('(%s)已运行%s秒'%(processID,(momentTime-startTime)))
                break#解析下一个token
            else:
                #还有下一页,继续解析
                followList=parseClass.parseFollow()
                for i in followList:
                    r.sadd('newID',i)
                n+=20

def parseMessage(processID):
    '''
    解析所有已爬token
    :param processID: 进程编号,justForTest
    :return: None
    '''

if __name__=='__main__':
    initID='f3lix'

    #建立redis池连接
    pool=redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)
    r=redis.Redis(connection_pool=pool)

    httpClass = Http()
    startTime=time.time()
    if Spider(initID):
        print('ojerk')