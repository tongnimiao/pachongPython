from lagouwang.parse import parsePage,parse
from lagouwang.https import Http
from lagouwang.setting import cookies,headers
import pandas

#主函数逻辑
def main(url,formData):
    if url:
        info=getINFO(url,formData)
        message=messageINFO(info)
        return message
    else:
        return None

#信息获取
def getINFO(url,formData):
    htmlINFO=Http()
    res=htmlINFO.post(url,formData=formData,headers=headers,cookies=cookies)
    pageCount,totalCount=parsePage(res)
    print('相关职位数量：%s'%totalCount)
    info=[]
    for i in range(1,pageCount+1):
        formData['pn']=str(i)
        res = htmlINFO.post(url, formData=formData, headers=headers, cookies=cookies)
        A,B=parse(res, totalCount)
        info=info+A
        totalCount=B
    return info

#信息存储
def messageINFO(message):
    df = pandas.DataFrame(message)
    df.to_excel('%s.xlsx'%position)
    return True

if __name__=='__main__':
    position='武汉'
    kd='python'     #相关职位信息
    url='https://www.lagou.com/jobs/positionAjax.json'
    formData={'first': "true",'pn': 1,'kd': kd,'city': position}
    print('开始爬取(%s %s)相关职位信息'%(position,kd))
    process=main(url,formData)
    if process:
        print('成功爬取(%s %s)相关职位信息'%(position,kd))
    else:
        print('爬取失败')