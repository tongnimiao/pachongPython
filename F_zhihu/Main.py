from F_zhihu.Parser import Json
from F_zhihu.Https import Http
from F_zhihu import Setting
import getProxy,random

def Spider(initID):
    allFollowID(initID)#爬取所有关注者及子孙关注者ID
    generateDoc()#生成文档

def allFollowID(initID):
    newID.add(initID)
    while len(newID)!=0:
        A=newID.pop()#bug
        n=0
        while True:
            followUrl=Setting.followUrl.format(id=A,page=n)
            htmlCode=httpClass.get(followUrl,
                                   headers={'User-Agent':random.choice(Setting.UA),
                                            'Cookie':random.choice(Setting.Cookies)},
                                   proxies={'proxy':random.choice(proxyPool)})
            if htmlCode==None:
                oldID.add(A)
                break
            parseClass = Json(htmlCode)
            if parseClass.isEnd() == True:
                followList=parseClass.parseFollow()
                for i in followList:
                    newID.add(i)
                oldID.add(A)
                print(newID)
                print('未解析ID长度%s:'%len(newID))
                print('已解析ID长度%s:'%len(oldID))
                break
            else:
                followList=parseClass.parseFollow()
                for i in followList:
                    newID.add(i)
                n+=20

def generateDoc():
    totalID = '*'.join(map(str, oldID))
    with open('totalID', 'w') as f:
        f.write(totalID)

if __name__=='__main__':
    initID='ju-zi-pi-92-44'
    proxyPool=getProxy.getProxy(1)#获取代理池
    newID=set()#未爬的ID去重List
    oldID=set()#已爬的ID去重List
    httpClass = Http()
    if Spider(initID):
        print('it\'s easy')