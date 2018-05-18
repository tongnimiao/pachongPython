import json
import mysql.connector

class Json(object):
    def __init__(self,htmlCode):
        self.htmlCode=htmlCode
        self.json=json.loads(htmlCode)

    def isEnd(self):
        '''
        判断关注者是否是最后一页
        :return:
        '''
        if self.json['paging']['is_end'] == True:
            return True
        elif self.json['paging']['is_end']==False:
            return False

    def isZeroFollow(self):
        '''
        判断是否没有关注者
        :return:
        '''
        if self.json['paging']['totals']==0:
            return True
        else:
            return False

    def parseFollow(self):
        '''
        解析newID[0]
        :return: 当页关注者用户token
        '''
        pageToken=[i['url_token'] for i in self.json['data']]
        return pageToken

    def parseMessage(self):
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
        name=self.json['name']
        token=self.json['url_token']
        gender=self.json['gender']
        following=self.json['following_count']
        followed=self.json['follower_count']
        vetoed=self.json['voteup_count']
        thanked=self.json['thanked_count']
        favorit=self.json['favorited_count']
        answerCount=self.json['answer_count']
        article=self.json['articles_count']
        questionCount=self.json['question_count']

        if len(self.json['educations'])==0:
            education=None
            eduProfession=None
        else:
            if 'school' in self.json['educations'][0]:
                education=self.json['educations'][0]['school']['name']
            else:
                education=None
            if 'major' in self.json['educations'][0]:
                eduProfession=self.json['educations'][0]['major']['name']
            else:
                eduProfession=None

        if 'business' not in self.json:
            business=None
        else:
            business=self.json['business']['name']

        if len(self.json['locations'])==0:
            location=None
        else:
            location=self.json['locations'][0]['name']

        if len(self.json['employments'])==0:
            employment=None
            empJob=None
        else:
            if 'company' in self.json['employments'][0]:
                employment=self.json['employments'][0]['company']['name']
            else:
                employment=None
            if 'job' in self.json['employments'][0]:
                empJob=self.json['employments'][0]['job']['name']
            else:
                empJob=None

        self.store2Mysql(name,token,gender,following,followed,vetoed,thanked,favorit,answerCount,article,questionCount,education,eduProfession,business,location,employment,empJob)

    def store2Mysql(self,name,token,gender,following,followed,vetoed,thanked,favorit,answerCount,article,questionCount,education,eduProfession,business,location,employment,empJob):

        cnn = mysql.connector.connect(user='root',password='0202508',database='zhihuSpider')
        cursor = cnn.cursor()
        print('insert into zhihuMessage values(default,\'%s\',\'%s\',%s,%s,%s,%s,%s,%s,%s,%s,%s,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(name,token,gender,following,followed,vetoed,thanked,favorit,answerCount,article,questionCount,education,eduProfession,business,location,employment,empJob))
        cursor.execute('insert into zhihuMessage values(default,\'%s\',\'%s\',%s,%s,%s,%s,%s,%s,%s,%s,%s,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(name,token,gender,following,followed,vetoed,thanked,favorit,answerCount,article,questionCount,education,eduProfession,business,location,employment,empJob))
        cnn.commit()
        cursor.close()
        cnn.close()