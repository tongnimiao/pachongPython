import requests
from bs4 import BeautifulSoup
import json
import pandas
import random
import time


def laGou(job,position=None):
    x=1
    message=[]
    formData={
        'first':"true",
        'pn':1,
        'kd':job,
        'city':position
    }
    headers={
        'Host':'www.lagou.com',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Referer':'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        'X-Anit-Forge-Code':'0',
        'X-Anit-Forge-Token':'None',
        'X-Requested-With':'XMLHttpRequest'
    }
    url='https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    res=requests.post(url,data=formData,headers=headers)
    resultSize=(json.loads(res.text))['content']['positionResult']['resultSize']
    totalCount= (json.loads(res.text))['content']['positionResult']['totalCount']
    if int(totalCount)%int(resultSize)==0:
        pageCount=int(totalCount)//int(resultSize)
    else:
        pageCount=int(totalCount)//int(resultSize)+1

    for i in range(pageCount):
        formData={
            'first':"true",
            'pn':i+1,
            'kd':job,
            'city':position
        }
        headers={
            'Host':'www.lagou.com',
            'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Referer':'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
            'X-Anit-Forge-Code':'0',
            'X-Anit-Forge-Token':'None',
            'X-Requested-With':'XMLHttpRequest'
        }

        url='https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

        res=requests.post(url,data=formData,headers=headers)
        list=(json.loads(res.text))['content']['positionResult']['result']

        print('Page:%s' %i)






        n=0
        for i in list:
            n+=1
            demand={}
            demand['公司全称']=i['companyFullName']
            demand['职位标签']=i['positionLables']
            demand['公司领域']=i['industryField']
            demand['发布日期']=i['createTime']
            demand['工作区域']=i['district']
            demand['工作经验']=i['workYear']
            demand['学历要求']=i['education']
            demand['公司优势']=i['positionAdvantage']
            demand['职位薪资']=i['salary']
            demand['公司规模']=i['companySize']
            demand['职业名称']=i['positionName']
            demand['工作方向']=i['firstType']
            time.sleep(random.random() * 3)
            if n%5==0:
                time.sleep(5.1)
            demand['职位描述']=(positionDescribe(i['positionId']))[0:250]
            message.append(demand)
            print('Count:%s'%x)
            print('ok')
            print('\n')
            x+=1


    df = pandas.DataFrame(message)
    df.to_excel('1.xlsx')
    print('Success!')

def positionDescribe(positionId):

    url='https://www.lagou.com/jobs/%s.html'

    headers={
        'Host':'www.lagou.com',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.5',
        'Accept-Encoding':'gzip, deflate, br',
        'Referer':'https://www.lagou.com/jobs/list_python?px=default&city=%E5%85%A8%E5%9B%BD',
        'Cookie':'_ga=GA1.2.680668695.1522371002; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522371002,1522373336,1522375507,1522627782; user_trace_token=20180330085001-4723e91f-33b4-11e8-a4c7-525400f775ce; LGUID=20180330085001-4723ed0c-33b4-11e8-a4c7-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAAAFCAAEG67F7206E08F6AB04F356BC5408EE827D; _gid=GA1.2.710371733.1522627782; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522630353; LGSID=20180402080941-240fb2b1-360a-11e8-ac76-525400f775ce; LGRID=20180402085232-2019f686-3610-11e8-ac79-525400f775ce; TG-TRACK-CODE=search_code; SEARCH_ID=465aab3f28ae4734ae9e90b452ee5bfc; _gat=1',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'Cache-Control':'max-age=0'
    }
    cookies={
        'ga':"GA1.2.680668695.1522371002",
        'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6':"1522371002,1522373336,1522375507,1522627782",
        'user_trace_token':"20180330085001-4723e91f-33b4-11e8-a4c7-525400f775ce",
        'LGUID':"20180330085001-4723ed0c-33b4-11e8-a4c7-525400f775ce",
        'index_location_city':"å\u0085¨å\u009b½",
        'JSESSIONID':"ABAAABAAAFCAAEG67F7206E08F6AB04F356BC5408EE827D",
        '_gid':"GA1.2.710371733.1522627782",
        'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6':"1522630353",
        'LGSID':"20180402080941-240fb2b1-360a-11e8-ac76-525400f775ce",
        'LGRID':"20180402085232-2019f686-3610-11e8-ac79-525400f775ce",
        'TG - TRACK - CODE':"search_code",
        'SEARCH_ID':"465aab3f28ae4734ae9e90b452ee5bfc",
        '_gat':"1"
    }

    res=requests.get(url%positionId,headers=headers,cookies=cookies)
    soup=BeautifulSoup(res.text,'lxml')
    str=(soup.select('.job_bt'))[0].text
    return str

laGou('python','广州')