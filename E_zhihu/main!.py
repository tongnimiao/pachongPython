from E_zhihu.setting import url,followUrl,headers
from E_zhihu.https import Http
from E_zhihu.parse import jsonParse,htmlParse
from getProxy import getProxy
import time,random,pandas


def main(tokenList,proxylist):
    '''
    解析一个token下的
    :param tokenList:
    :param proxylist:
    :return:
    '''
    tokenBigList=[]
    global layer
    layer+=1
    for token in tokenList:
        if token in totalToken:
            pass
        else:
            #页面解析Message
            parseMessage(token,proxylist)
            #关注人解析
            tokenLittleList=getFollowTotal(token,proxylist)
            tokenBigList=tokenBigList+tokenLittleList
            print(len(tokenBigList))
    main(tokenBigList,proxylist)
    return True

def getFollowTotal(token,proxylist):
    '''
    对关注人页面进行解析
    judge: 判断是否继续标志
    offset: 页面代码
    tokenList: 关注人token的list
    :return: 关注人token的list
    '''
    judge=True
    offset=0
    tokenList=[]
    while judge is True:
        pageCode= startHttp.get(followUrl.format(user=token, offset=offset), headers=headers,proxies={'proxy': random.choice(proxylist)})
        if pageCode==None:
            offset+=20
            continue
        followParse=htmlParse(pageCode)
        tokens=followParse.parseFollowing()
        tokenList=tokenList+tokens
        judge=followParse.parseEnd()
        offset+=20
        time.sleep(1)
        print('爬虫deep:%s'%layer)
        print('page:%s'%offset)
    return tokenList

def parseMessage(id,proxylist):
    '''
    对信息页面进行解析
    :param id: 检索ID
    :param proxylist: 代理IP
    '''
    #startHttp的get方法返回startCode,代理IP列表proxylist
    Code=startHttp.get(url.format(user=id),headers=headers,proxies={'proxies':random.choice(proxylist)})
    if Code == None:
        pass
    else:
        #将startParse设未jsonparse类,并传入startCode属性
        startParse=jsonParse(Code)
        #调用parseMessage方法进行解析,返回需求信息列表message和标签startToken
        messageDict=startParse.parseMessage()
        #在totalToken中添加已解析标签
        totalToken.append(id)
        #信息存储
        store(messageDict,id)
    time.sleep(1)

def store(messageDict,token):
    '''
    信息存储
    :param messageDist: 将存储的信息
    '''
    print(('%s------%s'%(token,messageDict)))
    print('爬取数目：'+str(len(totalToken)))
    global df
    df2=pandas.DataFrame([messageDict])
    df=df.append(df2)
    print(df)

if __name__=='__main__':
    #从此ID开始对知乎进行检索
    initialID=['ling-lin-41-66']
    #设置总标签检索列表totalToken,用来判断是否重复
    totalToken=[]
    #爬虫层数
    layer=1
    #创建一个空Df表
    df=pandas.DataFrame()
    #将startHttp设为Http类
    startHttp=Http()
    #获取初始代理IP列表
    proxylist=getProxy(1)
    #对初始页面进行解析
    parseMessage(initialID[0],proxylist)
    tokenlist=getFollowTotal(initialID[0],proxylist)
    #执行主逻辑函数
    if main(tokenlist,proxylist):
        print('知乎爬虫完成')
        df.to_excel('知乎')
    else:
        print('die')