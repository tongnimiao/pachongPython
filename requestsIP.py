import os,time,requests
from bs4 import BeautifulSoup

def fetch_proxy(num):
    os.chdir('/home/ot/桌面/pachong')
    api='http://www.xicidaili.com/nn/{}'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    fp=open('pachongIP','a+',encoding=('utf-8'))
    for i in range(num+1):
        api=api.format(1)
        respones=requests.get(url=api,headers=header)
        soup=BeautifulSoup(respones.text,'lxml')
        container=soup.find_all(name='tr',attrs={'class':'odd'})
        for tag in container:
            try:
                con_soup = BeautifulSoup(str(tag), 'lxml')
                td_list = con_soup.find_all('td')
                ip = str(td_list[1])[4:-5]
                port = str(td_list[2])[4:-5]
                IPport = ip + '\t' + port + '\n'
                fp.write(IPport)
            except Exception as e:
                print('No IP！')
        time.sleep(1)
    fp.close()
fetch_proxy(10)