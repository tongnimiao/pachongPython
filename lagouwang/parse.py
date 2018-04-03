import requests,json,time,random
from bs4 import BeautifulSoup
from collections import OrderedDict
from lagouwang.setting import headers,cookies

#获取页面数/项目总数的函数
def parsePage(res):
    resultSize = (json.loads(res))['content']['positionResult']['resultSize']
    totalCount = (json.loads(res))['content']['positionResult']['totalCount']
    if int(totalCount) % int(resultSize) == 0:
        pageCount = int(totalCount) // int(resultSize)
    else:
        pageCount = int(totalCount) // int(resultSize) + 1
    return pageCount,totalCount

#获取页面中职位的函数
def parse(res,totalCount):
    n,a=0,0
    message=[]
    list=(json.loads(res))['content']['positionResult']['result']
    for i in list:
        n += 1
        demand = OrderedDict()
        demand['公司全称'] = i['companyFullName']
        demand['工作经验'] = i['workYear']
        demand['学历要求'] = i['education']
        demand['职位薪资'] = i['salary']
        demand['职位名称'] = i['positionName']
        demand['职位标签'] = i['positionLables']
        demand['工作方向'] = i['firstType']
        demand['公司规模'] = i['companySize']
        demand['公司领域'] = i['industryField']
        demand['公司优势'] = i['positionAdvantage']
        demand['工作区域'] = i['district']
        demand['发布日期'] = i['createTime']
        time.sleep(random.random() * 3)
        if n % 5 == 0:
            time.sleep(5.1)
        demand['职位描述'] = (positionDescribe(i['positionId']))[0:250]
        message.append(demand)
        totalCount-=1
        print('成功，剩余数量%s'%totalCount)
    return message,totalCount

#获取职位描述的函数
def positionDescribe(positionId):
    url='https://www.lagou.com/jobs/%s.html'
    res=requests.get(url%positionId,headers=headers,cookies=cookies)
    soup=BeautifulSoup(res.text,'lxml')
    str=(soup.select('.job_bt'))[0].text
    return str