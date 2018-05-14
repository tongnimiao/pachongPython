import json

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

    def parseFollow(self):
        '''
        解析newID[0]
        :return: 当页关注者用户token
        '''
        pageToken=[i['url_token'] for i in self.json['data']]
        return pageToken