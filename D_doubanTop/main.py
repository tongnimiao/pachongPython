from D_doubanTop.parse import parseMovieHome,parseMusicHome,parseBookHome,parseMovie,parseMusic,parseBook,saveMessage
from D_doubanTop.setting import headers
from Z_getProxy.getProxy import getProxy
import time

def main(kind):
    #用来存储的总list
    totalList=[]
    #更改Referer,告知网页出处
    headers['Referer']='https://%s.douban.com/chart'%kind
    #开始页面,0等于从1开始
    Num=0
    #生成代理IP池
    proxys=getProxy(1)
    #250条信息,单页25条信息,需要循环10次
    for i in range(10):
        #生成URL,eg.movie
        homeUrl='http://'+kind+'.douban.com/top250?start='+str(Num)
        #判断种类，根据种类解析Movie
        if kind=='movie':
            #解析Top250主页面,返回内文URL
            pageUrlList=parseMovieHome(homeUrl,proxys)
            #开始抓取内文提示
            print('\n链接豆瓣{}TOP250第{}页信息成功(剩余{}页)'.format(kind,i+1,9-i))
            #解析单个页面,返回需要信息(电影名/年份/评分/评分人数/标签/剧情简介/)
            totalList=totalList+parseMovie(pageUrlList,proxys)
        #判断种类，根据种类解析Music
        elif kind=='music':
            #解析Top250主页面,返回内文URL
            pageUrlList=parseMusicHome(homeUrl,proxys)
            #开始抓取内文提示
            print('\n链接豆瓣{}TOP250第{}页信息成功(剩余{}页)'.format(kind,i+1,9-i))
            #解析单个页面,返回需要信息(专辑名/表演者/评分/评分人数/流派/专辑类型/介质/发行时间/出版者/条形码/ISRC/简介/曲目)
            totalList=totalList+parseMusic(pageUrlList,proxys)
        #判断种类，根据种类解析Book
        elif kind=='book':
            #解析Top250主页面,返回内文URL
            pageUrlList=parseBookHome(homeUrl,proxys)
            #开始抓取内文提示
            print('\n链接豆瓣{}TOP250第{}页信息成功(剩余{}页)'.format(kind,i+1,9-i))
            #解析单个页面,返回需要信息(名字/作者/评分/评分人数/出版年/页数/ISBC/内容简介)
            totalList=totalList+parseBook(pageUrlList,proxys)
        #HomeUrl更换
        Num+=25
    #存储信息excel
    saveMessage(totalList,kind)
    #结束movie循环
    return True

if __name__=='__main__':
    #请输入浏览器保存豆瓣Cookie
    headers['Cookie']=''
    #种类：movie/music/book
    kind=['movie','music','book']
    for i in kind:
        starttime=time.time()
        if main(i):
            endtime=time.time()
            print('\n完成豆瓣{}TOP250抓取,用时:{}分{}秒'.format(kind,(endtime-starttime)//60,(endtime-starttime)%60))
        else:
            print('获取失败')