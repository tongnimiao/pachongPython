class urlManager(object):
    def __init__(self):
        self.newUrls=set()#未爬url
        self.oldUrls=set()#已爬url

    def newOrOldUrl(self):
        '''
        判断是否有新的URL
        :return:
        '''
        return self.newUrlSize()!=0

    def getNewUrl(self):
        '''
        获取一个未爬的URL
        :return:
        '''
        newUrl=self.newUrls.pop()
        self.oldUrls.add(newUrl)
        return newUrl

    def addNewUrl(self,url):
        '''
        将新的URL添加到未爬URL集合中
        :param url:
        :return:
        '''
        if url is None:
            return
        elif url not in self.newUrls and url not in self.oldUrls:
            self.newUrls.add(url)

    def addNewUrls(self,urls):
        '''
        将新的URLLIST添加到未爬URL集合中
        :param urls:
        :return:
        '''
        if urls is None or len(urls)==0:
            return
        for i in urls:
            self.addNewUrl(i)

    def newUrlSize(self):
        '''
        获取未爬URL集合大小
        :return:
        '''
        return len(self.newUrls)

    def oldUrlSize(self):
        '''
        获取已爬URL集合大小
        :return:
        '''
        return len(self.oldUrls)