from F_zhihu.Parser import Json
from F_zhihu.Https import Http
from F_zhihu import Setting
from multiprocessing import Pool
import random,time,redis
from Z_getProxy import getProxy
def Main():
    p=Pool(15)
    for i in range(15):
        print('sleeping')
        time.sleep(i)
        print('sleeped')
        p.apply_async(Spider,args=(i,))
    p.close()
    p.join()


def Spider(processID):
    allFollowID(processID)
    time.sleep(20)
    parseMessage(processID)


def allFollowID(processID):
    '''
    爬取所有关注者及子孙关注者token
    :param processID: 进程编号,justForTest
    :return: None
    '''
    print(1)
    while True:
        print('googingggg')
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
        print(A)
        htmlCode=httpClass.get(Setting.followUrl.format(id=A,page=n),
                      headers={'User-Agent':random.choice(Setting.UA),'Cookie':random.choice(Setting.Cookies)},
                      proxies={'proxy':proxy})
        print(htmlCode)
        while True:


            #访问失败跳过该token
            if htmlCode==None:
                r.sadd('oldID',A)
                r.srem('proxy',proxy)
                break


            parseClass = Json(htmlCode)
            if parseClass.isZeroFollow()==True:
                r.sadd('oldID',A)
                break

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
    while True:
        #检测代理的剩余量,补充及大休眠
        if r.scard('proxy') < 10:
            if processID==0:
                getProxy.getProxy()
            time.sleep(100)

        #检测爬虫是否完成
        if r.scard('oldID')==0:
            time.sleep(20)
            if r.scard('oldID')==0:
                print('(%s)号信息结束'%processID)
                break
            else:
                continue

        #随机获取并解析
        parseToken=r.spop('oldID')
        messageUrl='https://www.zhihu.com/api/v4/members/{token}?include=name,url_token,educations,business,locations,employments,gender,following_count,follower_count,voteup_count,thanked_count,favorited_count,answer_count,articles_count,question_count.topics'
        proxy=r.srandmember('proxy')
        htmlCode=httpClass.get(messageUrl.format(token=parseToken),
                      headers={'User-Agent':random.choice(Setting.UA),'Cookie':random.choice(Setting.Cookies)},
                      proxies={'proxy':proxy})
        #访问失败跳过,过会重来
        if htmlCode == None:
            r.srem('proxy',proxy)
            r.sadd('oldID',parseToken)
            continue

        #存储2MySQL DB:zhihuSpider
        parseClass=Json(htmlCode)
        parseClass.parseMessage()

if __name__=='__main__':
    #建立redis池连接
    pool=redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)
    r=redis.Redis(connection_pool=pool)

    httpClass = Http()
    startTime=time.time()
    if Main():
        print('ojerk')