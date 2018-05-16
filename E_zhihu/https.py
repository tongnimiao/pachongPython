from Z_getProxy.getProxy import getProxy
from E_zhihu.setting import UA
import requests,random,logging

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s Process%(process)d:%(thread)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logging.log',
                    filemode='a')

class Http(object):
    '''
    定义请求
    '''
    def get(self,url,headers=None,proxies=None,timeout=5,timeoutRetry=5):
        '''
        :param url: 目标URL
        :param headers: 请求头
        :param proxies: 代理IP
        :param timeout: 超时时间
        :param timeoutRetry: 超时次数
        :return: respone
        '''
        if not headers:
            headers={'User-Agent':random.choice(UA),
                     'Cookie': '__DAYU_PP=6NEQzBVeevByUuMjrEzEffffffff8a15a08bae39; q_c1=9c46a0fb9939422881967decd788e462|1521676280000|1521676280000; _zap=fd45d673-aa0f-4999-ae2d-57dce5ceae92; l_cap_id="MTVhZTgwMmE2NjJmNDU3ZjliYWNmYzMyNjdiZTAzODE=|1524095802|97edbda534c1a22c5d8db4392a9179c1d21b400e"; r_cap_id="MDVjMDY3MDk0YjkwNGFhNWI2NDkwM2FiNzdlOThmN2U=|1524095802|0b58fcce4bf7e66bf1184ac9e18e0ee5bb697c93"; cap_id="YTljOWU3ZDQ2YWZjNDBlZGFiMzBkMWZkYTIzNDljZjQ=|1524095802|c914e7f3996b7dac4464d21b80c67f46ef35b4fb"; capsion_ticket="2|1:0|10:1524095932|14:capsion_ticket|44:ZGU5NzQwZjE2Mjk0NDJmNDhiMjIyNTRiZmU5ZWVmNmM=|be383318d21315d6c3b0b662368773b0223a71e1bf5e6426a12aa94e5a8e0221"; __utma=155987696.1438037459.1523587187.1523587187.1523955550.2; __utmz=155987696.1523587187.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aliyungf_tc=AQAAANWDWRwK9AEAjDIUOoWFTi0g+Pvf; _xsrf=c860fc1b-7a7d-46c8-ae16-3ef95d1dbe1f; d_c0="ALAvfaeYdA2PTopEc437l1BsFz92c33MUBE=|1523942945"; l_n_c=1; n_c=1; __utmc=155987696; z_c0="2|1:0|10:1524095942|4:z_c0|92:Mi4xbWJaS0JnQUFBQUFBc0M5OXA1aDBEU1lBQUFCZ0FsVk54aW5GV3dDUGY2Z3F1R29xNTZwekVaSXJ3WG90Y2RnVmNR|0227ba78d786d9e305d14d06d65e7a232bc6c03555df0ffcc52a4206a1f9b5f4"'
            }
        if not proxies:
            proxylist=getProxy(1)
            proxies={'proxies':random.choice(proxylist)}
        '''
        requests.get请求
        '''
        try:
            res=requests.get(url,headers=headers,proxies=proxies,timeout=timeout)
            res.raise_for_status()
            htmlCode=res.text
        except Exception as e:
            logging.error('getEXCEPT:{}'.format(e))
            if timeoutRetry>0:
                proxylist=getProxy(1)
                htmlCode=self.get(url=url,headers=headers,proxies=random.choice(proxylist),timeoutRetry=timeoutRetry-1)
            else:
                logging.error('getTIMEOUT:{}'.format(url))
                htmlCode=None
        return htmlCode