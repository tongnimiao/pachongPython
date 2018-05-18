from F_zhihu import Setting
from Z_getProxy.getProxy import getProxy
import requests,random,logging,time,redis
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logging.log',
                    filemode='a')

class Http(object):
    def get(self,url,headers=None,proxies=None,timeout=10,timeoutRetry=5):
        '''
        get方法
        :param url:目标url
        :param headers: 请求头
        :param proxies: 代理IP
        :param timeout: 超时时间
        :param timeoutRetry: 超时次数
        :return:
        '''
        if not headers:
            headers = {'User-Agent': random.choice(Setting.UA), 'Cookie': random.choice(Setting.Cookies)}

        if not proxies:
            pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
            r = redis.Redis(connection_pool=pool)
            proxy=r.srandmember('proxy')
            proxies={'proxy':proxy}
            print('重连的代理为%s'%proxies)

        try:
            res=requests.get(url,headers=headers,proxies=proxies,timeout=timeout)
            res.raise_for_status()
            htmlCode=res.text
        except Exception as e:
            logging.error('getExcept:{}'.format(e))
            if timeoutRetry>0:
                htmlCode=self.get(url=url,timeoutRetry=timeoutRetry-1)
            else:
                logging.error('getTimeout:{}'.format(url))
                htmlCode=None
        time.sleep(1.5)
        return htmlCode