import os
import time
import requests
from bs4 import BeautifulSoup
def test_proxy():
    N = 1
    os.chdir('/home/ot/桌面/pachong')
    url = 'https://www.baidu.com'
    fp = open('pachongIP', 'r')
    ips = fp.readlines()
    proxys = list()
    for p in ips:
        ip = p.strip('\n').split('\t')
        proxy = 'http:\\' + ip[0] + ':' + ip[1]
        proxies = {'proxy': proxy}
        proxys.append(proxies)
    for pro in proxys:
        try:
            s = requests.get(url, proxies=pro)
            print('第{}个ip：{} 状态{}'.format(N,pro,s.status_code))
        except Exception as e:
            print(e)
        N+=1

test_proxy()