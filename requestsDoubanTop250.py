import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL='https://movie.douban.com/top250'
def downloadPage(Url):

    headers={
        'User-Agent':'Mozilla/5.0(Macintosh;Intel Mac OS X 10_11_2)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'    #模拟浏览器绕过UA反爬
    }

    data=requests.get(Url,headers=headers).content  #将UA信息加入请求HEAD
    return data

def main():
    print(downloadPage(DOWNLOAD_URL))

def parseHtml(html):
    soup=BeautifulSoup(html)
    movieListSoup=soup.find('ol',attrs={'class':'grid_view'})
    for movieLi in movieListSoup.find_all('li'):
        detail=movieLi.find('div',attrs={'class':'hd'})
        movieName=detail.find('span',attrs={'class':'title'}).getText()
        print(movieName)
if __name__=='__main__':
    main()