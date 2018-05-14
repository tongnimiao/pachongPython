import requests
from bs4 import BeautifulSoup


header={
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0',
}
res=''
try:
    res=requests.get('http://seputu.com',headers=header)
    res.raise_for_status()
    soup=BeautifulSoup(res.text,'lxml')
    num=0
    for i in soup.select('.bg .mulu .box ul li'):
        neiwenUrl=i.select('a')[0].get('href')
        try:
            neiwenRes = requests.get(neiwenUrl,headers=header)
            neiwenRes.raise_for_status()
            neiwenRes.encoding='utf-8'
            neiwenSoup = BeautifulSoup(neiwenRes.text, 'lxml')
            title=neiwenSoup.select('.bg h1')[0].text
            str=''
            for a in neiwenSoup.select('.bg .content-body p'):
                str=str+'\n'+a.text
            neiwen=str.replace('http://seputu.com/','').replace('www.seputu.com','')
            with open('test','a') as f:
                f.write(title+'\n'+neiwen+'\n\n\n')
            num+=1
            print(num)
        except Exception as e:
            print('badCode')
except Exception as e:
    print('badCode')