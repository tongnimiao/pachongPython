import requests
from bs4 import BeautifulSoup
import json
import pandas
import os


def laGou(page,job,position=None):
    message=[]
    formData={
        'first':"true",
        'pn':page,
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
    for i in list:
        demand={}
        print(i['positionId'])
        demand['职位描述']=positionDescribe(i['positionId'])
        demand['公司名称']=i['companyShortName']
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
        message.append(demand)

    df = pandas.DataFrame(message)
    df.to_excel('test.xlsx')
    print('Success!')

def positionDescribe(positionId):

    url='https://www.lagou.com/jobs/%s.html'

    headers={
        'Host':'www.lagou.com',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Referer':'https://www.lagou.com/jobs/list_python?px=default&city=%E5%85%A8%E5%9B%BD',
    }

    res=requests.get(url%positionId,headers=headers)
    soup=BeautifulSoup(res.text,'lxml')
    str=(soup.select('.job_bt'))[0].text
    return str

laGou(1,'python')