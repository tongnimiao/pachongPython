from bs4 import BeautifulSoup
import requests,time,re,pandas,random
from collections import OrderedDict
from doubanTop.setting import headers,UserAgent

def parseMovieHome(url,proxys):
    headers['User-Agent']=random.choice(UserAgent)
    res=requests.get(url,headers=headers,proxies=random.choice(proxys))
    soup=BeautifulSoup(res.text,'lxml')
    return [i['href'] for i in soup.select('.info a')]

def parseMusicHome(url,proxys):
    headers['User-Agent']=random.choice(UserAgent)
    res=requests.get(url,headers=headers,proxies=random.choice(proxys))
    soup=BeautifulSoup(res.text,'lxml')
    return [i['href'] for i in soup.select('.item .nbg')]

def parseBookHome(url,proxys):
    headers['User-Agent']=random.choice(UserAgent)
    res=requests.get(url,headers=headers,proxies=random.choice(proxys))
    soup=BeautifulSoup(res.text,'lxml')
    return [i['href'] for i in soup.select('.item .nbg')]

def parseMovie(urlList,proxys):
    message10List=[]
    for i in urlList:
        movieMessage=OrderedDict()
        headers['User-Agent']=random.choice(UserAgent)
        res=requests.get(i,headers=headers,proxies=random.choice(proxys))
        soup=BeautifulSoup(res.text,'lxml')
        nameDate=soup.select('#content h1')[0].text.replace('\n','')
        reg=re.compile(r'(.+)\((\d+)')
        score=soup.select('#interest_sectl div div')[0].next_sibling.next_sibling.text.replace('\n','')
        reg2=re.compile(r'(\d+.\d)(.+)')
        movieMessage['电影名']=reg.search(nameDate).group(1)
        movieMessage['年份']=reg.search(nameDate).group(2)
        movieMessage['评分']=reg2.search(score).group(1)
        movieMessage['评分人数'] = reg2.search(score).group(2)
        movieMessage['标签']=soup.select('.tags-body')[0].text.strip('\n').replace('\n',',')
        movieMessage['剧情简介']=soup.select('#link-report')[0].text.replace(' ','').replace('\n','').replace('\u3000','')[0:250]
        message10List.append(movieMessage)
        time.sleep(2)
    return message10List

def parseMusic(urlList,proxys):
    message10List = []
    for i in urlList:
        musicMessage = OrderedDict()
        headers['User-Agent']=random.choice(UserAgent)
        res = requests.get(i, headers=headers,proxies=random.choice(proxys))
        soup=BeautifulSoup(res.text,'lxml')
        typeData=soup.select('#info')[0].text
        musicMessage['专辑名']=soup.select('#wrapper h1')[0].text.replace('\n','')
        musicMessage['表演者']=soup.select('#info span a')[0].text
        musicMessage['发行时间']=re.search(r'(\d{4}-\d{2}-\d{2})|(\d{4})',typeData).group()
        if re.search(r'流派:\s([\u4e00-\u9fa5]+)',typeData)!=None:
            musicMessage['专辑流派']=re.search(r'流派:\s([\u4e00-\u9fa5]+)',typeData).group(1)
        else:
            musicMessage['专辑流派']='--'
        musicMessage['评分']=soup.select('#interest_sectl div strong')[0].text
        musicMessage['评分人数']=soup.select('.rating_people')[0].text.rstrip('评价')
        musicMessage['标签']=soup.select('.tags-body')[0].text.strip('\n').replace('\n',',')
        if soup.select('.track-list'):
            musicMessage['曲目']=soup.select('.track-list')[0].text.replace('\n',' ').strip()
        else:
            str=''
            for i in soup.select('.song-items-wrapper ul li'):
                str=str+i.select('.song-name-short')[0].text.replace('\n', '')+','
            musicMessage['曲目']=str
        if soup.select('#link-report'):
            suggestE=re.findall(r'[a-z,A-Z]+',soup.select('#link-report')[0].text)
            suggestC=re.findall(r'[\u4e00-\u9fa5]',soup.select('#link-report')[0].text)
            if len(suggestE)<len(suggestC):
                musicMessage['简介']=soup.select('#link-report')[0].text.replace(' ','').replace('\n','').replace('\r','').replace('\u3000','')[0:250]
            else:
                musicMessage['简介']=soup.select('#link-report')[0].text.replace('\n','').replace('\r','').replace('\u3000','').strip()[0:250]
        else:
            musicMessage['简介']='--'
        message10List.append(musicMessage)
        time.sleep(2)
    return message10List

def parseBook(urlList,proxys):
    message10List = []
    for i in urlList:
        bookMessage = OrderedDict()
        headers['User-Agent']=random.choice(UserAgent)
        res = requests.get(i, headers=headers,proxies=random.choice(proxys))
        if res.status_code==200:
            soup=BeautifulSoup(res.text,'lxml')
            bookMessage['书名']=soup.select('#wrapper h1 span')[0].text
            bookMessage['作者']=soup.select('#info a')[0].text.replace('\n','').replace(' ','')
            bookMessage['出版年']=re.search(r'(\d{4}-\d{2})|(\d{4}-\d{1})|(\d{4})',soup.select('#info')[0].text).group()
            bookMessage['评分']=soup.select('.rating_num')[0].text.strip()
            bookMessage['评分人数']=soup.select('.rating_people')[0].text.rstrip('评价')
            bookMessage['内容简介']=soup.select('.intro')[0].text.replace('\n','').replace('\u3000','')[0:250]
            message10List.append(bookMessage)
        else:
            bookMessage['书名'] = '该书已消失在茫茫豆瓣中'
            message10List.append(bookMessage)
        time.sleep(1.1)
    return message10List

def saveMessage(List,kind):
    df=pandas.DataFrame(List)
    df.to_excel('豆瓣%sTop250.xlsx'%kind)
