import requests

class HtmlDownloader(object):
    def download(self,url):
        if url is None:
            return None
        user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
        headers={'User_Agent':user_agent}
        res=requests.get(url,headers=headers)
        if res.status_code==200:
            res.encoding='utf-8'
            return res.text
        return None