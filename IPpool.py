#生成代理池子，num为代理池容量
import os
def proxypool(num):
    n = 1
    os.chdir('/home/ot/桌面/pachong')
    fp = open('pachongIP', 'r')
    proxys = list()
    ips = fp.readlines()
    while n<num:
        for p in ips:
            ip = p.strip('\n').split('\t')
            proxy = 'http:\\' + ip[0] + ':' + ip[1]
            proxies = {'proxy': proxy}
            proxys.append(proxies)
            n+=1
    return proxys