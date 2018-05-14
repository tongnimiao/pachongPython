from getProxy import getProxy
from E_zhihu.setting import headers,url,followUrl
from E_zhihu.parse import jsonParse,htmlParse
from E_zhihu.https import Http
import logging,time,random

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s Process%(process)d:%(thread)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logging.log',
                    filemode='a')

def ot(id,proxylist):
    '''
    获取所有关注人的token
    '''

    judge=True
    startHttp=Http()
    offset=0
    while judge is not False:
        pageCode,proxylist=startHttp.get(followUrl.format(user=id,offset=offset),headers=headers,proxies={'proxy':random.choice(proxylist)},proxylist=proxylist)
        pageParse=htmlParse(pageCode)
        totalList=pageParse.parseFollowing()

        for i in totalList:
            if i not in totalToken:
                followCode,proxylist=startHttp.get(url=url.format(user=i),headers=headers,proxies={'proxy':random.choice(proxylist)},proxylist=proxylist)
                followParse=jsonParse(followCode)
                message,token=followParse.parseMessage()
                print(('%s------%s'%(id,message)))
                print('爬取数目：'+str(len(totalToken)))
                totalToken.append(token)
                time.sleep(2)
                ot(token,proxylist)
            else:
                pass
        judge=pageParse.parsePage()
        offset+=20


if __name__=='__main__':
    id='jixin'
    totalToken=[]
    '''
    通过用户关注页面获取url_token/通过is_end判断是否有下页/通过next获取下一页关注界面
    初始用户关注页面（只需user）
    https://www.zhihu.com/api/v4/members/{user}/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&limit=20&offset=0
    '''
    proxylist=getProxy(1)
    startHttp=Http()
    startCode,proxylist=startHttp.get(url.format(user=id),headers=headers,proxies={'proxy':'http://111.170.82.89:61234'},proxylist=proxylist)
    startParse=jsonParse(startCode)
    message,token=startParse.parseMessage()
    totalToken.append(token)
    ot(token,proxylist)
