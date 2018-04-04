import requests,datetime
from R12306.setting import trainAbbUrl,params
from R12306.parse import inputMessage,parseTrainAbb,parseTrainMessage,produceHeaders,printMessage,store

#主程序逻辑
def main():
    #导入起始站终点站日期信息
    inputMessage(fromStation,toStation,date)
    #获取车辆对应缩写列表
    abbDict=getTrainAbb()
    #根据站点和缩写列表生成对应Url
    stationUrl = 'https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=' + params['date'] + '&leftTicketDTO.from_station=' +abbDict[params['fromStation']] + '&leftTicketDTO.to_station=' + abbDict[params['toStation']] + '&purpose_codes=ADULT'
    #获取相关列车信息
    trainList=getTrainMessage(stationUrl)
    #打印并存储列车信息
    printAndStore(trainList)
    return True

#获取车辆对应缩写列表
def getTrainAbb():
    res = requests.get(trainAbbUrl)
    abbDict=parseTrainAbb(res)
    return abbDict

#获取车辆信息
def getTrainMessage(stationUrl):
    headers=produceHeaders(stationUrl)
    res = requests.get(stationUrl, headers=headers)
    res.encoding = 'utf-8'
    trainMessage=parseTrainMessage(res)
    return trainMessage

#打印&存储
def printAndStore(trainList):
    printMessage(trainList)
    store(trainList)

if __name__=='__main__':
    now=datetime.datetime.now().strftime('%Y-%m-%d')
    '''
        fromStation：起始站
        toStation：终点站
        date：查询日期(格式'20XX-XX-XX'或者now)
        now：今天的日期
    '''
    fromStation='常德'
    toStation='长沙'
    date='2018-04-10'

    yep=main()
    if yep:
        pass
    else:
        print('获取失败')