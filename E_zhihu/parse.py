import json
from collections import OrderedDict

class jsonParse(object):
    '''
    解析页面
    '''
    def __init__(self,htmlCode):
        self.htmlCode=htmlCode
        self.json=json.loads(htmlCode)

    def parseMessage(self):
        '''
        解析个人信息
        :return:个人信息dict
        '''
        messageDict=OrderedDict()
        messageDict['name'] =self.json['name']
        messageDict['sex'] =self.json['gender']
        messageDict['headline'] =self.json['headline']
        messageDict['photo'] =self.json['avatar_url_template'].format(size='xl')
        try:
            messageDict['location'] =self.json['locations'][0]['name']
        except Exception as e:
            messageDict['location'] =''
        try:
            messageDict['education'] =self.json['educations'][0]['school']['name']
        except Exception as e:
            messageDict['education'] =''
        return messageDict

class htmlParse(object):
    def __init__(self,htmlCode):
        self.htmlCode=htmlCode
        self.json=json.loads(htmlCode)

    def parseEnd(self):
        '''
        解析关注了的是否到end
        :return: 结束标识
        '''
        if str(self.json['paging']['is_end'])=='False':
            return True#继续
        else:
            return False#停止

    def parseFollowing(self):
        '''
        解析关注了信息
        :return:url_token
        '''
        tokens=[]
        for i in self.json['data']:
            token=i['url_token']
            tokens.append(token)
        return tokens