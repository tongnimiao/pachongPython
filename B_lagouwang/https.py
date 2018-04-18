from lagouwang.setting import User_Agent
import logging,random,requests
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Http:
    def __init__(self):
        pass

    def get(self,url,formData,headers=None,cookies=None):
        if not url:
            logging.error('getError Url not exist')
        try:
            if not headers:
                headers={'User-Agent':User_Agent[random.randint(0,len(User_Agent)-1)]}
            res=requests.get(url,formData,headers=headers,cookies=cookies)
            if res.status_code==200:
                htmlCode=res.text
            else:
                htmlCode=None
                logging.error('Get %s %s'%(str(res.status_code),url))
        except Exception as e:
            logging.error('getExcept %s' % str(e))
            htmlCode = None
        return htmlCode

    def post(self,url,formData,headers=None,cookies=None):
        if not url:
            logging.error('postError Url not exist')
        try:
            if not headers:
                headers={'User-Agent':User_Agent[random.randint(0,len(User_Agent)-1)]}
            res=requests.post(url,formData,headers=headers,cookies=cookies)
            if res.status_code==200:
                htmlCode=res.text
            else:
                htmlCode=None
                logging.error('Post %s %s'%(str(res.status_code),url))
        except Exception as e:
            logging.error('postExcept %s' % str(e))
            htmlCode = None
        return htmlCode