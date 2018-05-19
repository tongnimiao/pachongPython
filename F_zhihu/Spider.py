from F_zhihu.Parser import Json
from F_zhihu.Https import Http
from F_zhihu import Setting
from multiprocessing import Pool
import random,time,redis,json,mysql.connector
from Z_getProxy import getProxy

class Spider(Http):
    def AFCODE(self):
        while True:
            pass


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
        #检测代理的剩余量,补充
        if processID==0:
            if r.scard('proxy') < 30:
                getProxy.getProxy()

    def randomUrl(self,symbol,page):
        #随机获取token组成Url
        token=r.spop('unParse')
        if symbol=='allFollow':
            url = Setting.url[symbol].format(id=token, page=page)
        else:
            url = Setting.url[symbol].format(id=token)
        return token,url

    def requestsIt(self,symbol,page):
        token,url=self.randomUrl(symbol,page)
        proxy = r.srandmember('proxy')
        htmlCode=self.get(url,
                      headers={'User-Agent':random.choice(Setting.UA),'Cookie':random.choice(Setting.Cookies)},
                      proxies={'proxy':proxy})
        if htmlCode==None:
            self.add2AlParse(token)
            self.delPro(proxy)
        return htmlCode,token

    def add2AlParse(self,token):
        r.sadd('alParse',token)

    def add2UnParse(self,token):
        r.sadd('unParse',token)

    def delPro(self,proxy):
        r.srem('proxy',proxy)

    def toJson(self,htmlCode):
        Json=json.loads(htmlCode)
        return Json

    def isZeroFollow(self,Json):
        '''
        判断是否没有关注者
        :return:
        '''
        if Json['paging']['totals'] == 0:
            return True
        return False

    def isEnd(self,Json):
        '''
        判断关注者是否是最后一页
        :return:
        '''
        if Json['paging']['is_end'] == True:
            return True
        return False


    def parseFollow(self,Json):
        '''
        解析newID[0]
        :return: 当页关注者用户token
        '''
        tokenList = [i['url_token'] for i in Json['data']]
        return tokenList

    def parseAllFollow(self,symbol):
        page=0
        while True:
            htmlCode,token=self.requestsIt(symbol,page)
            if htmlCode==None:
                break
            Json=self.toJson(htmlCode)
            if self.isZeroFollow(Json)==True:
                self.add2AlParse(token)
                break
            if self.isEnd(Json)==True:
                for i in self.parseFollow(Json):
                    self.add2UnParse(i)
                self.add2AlParse(token)
                break
            for i in self.parseFollow(Json):
                self.add2UnParse(i)
            page+=20

    def parseMessage(self,symbol):
        htmlCode,token=self.requestsIt(symbol,0)
        if htmlCode!=None:
            Json=self.toJson(htmlCode)
            self.parseMessage(Json)

    def JsonMessage(self,Json):
        '''
        ID（非token）    not null  ['name']
        token           not null  ['url_token']
        性别             not null  ['gender']
        关注了多少人      not null  ['following_count']
        被多少人关注      not null  ['follower_count']
        获得赞同数       not null   ['voteup_count']
        获得感谢数       not null  ['thanked_count']
        获得收藏数       not null  ['favorited_count']
        回答次数         not null  ['answer_count']
        文章数          not null    ['articles_count']
        提问数          not null    ['question_count']

        学校                null  ['educations'][0]['school']['name']
        在校专业           null  ['educations'][0]['major']['name']
        从事行业            null   ['business']['name']
        居住地址             null  ['locations'][0]['name']
        职业经历            null  ['employments'][0]['company']['name']
        职业工作            null   ['employments'][0]['job']['name']

        https://www.zhihu.com/api/v4/members/ling-lin-41-66?include=name,url_token,educations,business,locations,employments,gender,following_count,follower_count,voteup_count,thanked_count,favorited_count,answer_count,articles_count,question_count.topics
        :return:
        '''
        name=Json['name']
        token=Json['url_token']
        gender=Json['gender']
        following=Json['following_count']
        followed=Json['follower_count']
        vetoed=Json['voteup_count']
        thanked=Json['thanked_count']
        favorit=Json['favorited_count']
        answerCount=Json['answer_count']
        article=Json['articles_count']
        questionCount=Json['question_count']

        if len(Json['educations'])==0:
            education=None
            eduProfession=None
        else:
            if 'school' in Json['educations'][0]:
                education=Json['educations'][0]['school']['name']
            else:
                education=None
            if 'major' in Json['educations'][0]:
                eduProfession=Json['educations'][0]['major']['name']
            else:
                eduProfession=None

        if 'business' not in Json:
            business=None
        else:
            business=Json['business']['name']

        if len(Json['locations'])==0:
            location=None
        else:
            location=Json['locations'][0]['name']

        if len(Json['employments'])==0:
            employment=None
            empJob=None
        else:
            if 'company' in Json['employments'][0]:
                employment=Json['employments'][0]['company']['name']
            else:
                employment=None
            if 'job' in Json['employments'][0]:
                empJob=Json['employments'][0]['job']['name']
            else:
                empJob=None

    def store2Mysql(self,name,token,gender,following,followed,vetoed,thanked,favorit,answerCount,article,questionCount,education,eduProfession,business,location,employment,empJob):

        cnn = mysql.connector.connect(user='root',password='0202508',database='zhihuSpider')
        cursor = cnn.cursor()
        print('insert into zhihuMessage values(default,\'%s\',\'%s\',%s,%s,%s,%s,%s,%s,%s,%s,%s,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(name,token,gender,following,followed,vetoed,thanked,favorit,answerCount,article,questionCount,education,eduProfession,business,location,employment,empJob))
        cursor.execute('insert into zhihuMessage values(default,\'%s\',\'%s\',%s,%s,%s,%s,%s,%s,%s,%s,%s,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(name,token,gender,following,followed,vetoed,thanked,favorit,answerCount,article,questionCount,education,eduProfession,business,location,employment,empJob))
        cnn.commit()
        cursor.close()
        cnn.close()

    def changeMode(self):
        r.sunionstore('unParse','unParse','alParse')
        r.delete('alParse')
def main(processID):
    '''
    运行总步骤
    :param processID:编号--Just For Test
    '''
    while True:
        if spider.completed('unParse')==True:#没有可爬--跳出
            break
        spider.proxyCount(processID)#检测代理数量
        spider.parseAllFollow('allFollow')#爬取所有人的token
    time.sleep(100)
    spider.changeMode()
    while True:
        if spider.completed('unParse')==True:
            break
        spider.proxyCount(processID)
        spider.parseMessage('message')
    spider.store2Mysql()

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
