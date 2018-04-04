from R12306.setting import cookies,headers,params
from collections import OrderedDict
import re,json,pandas

def inputMessage(fromStation,toStation,date):
    params['fromStation']=fromStation
    params['toStation']=toStation
    params['date']=date

def parseTrainAbb(res):
    reg = re.compile(r'([\u4e00-\u9fa5]+)\|([A-Z]{3})')
    dict = {}
    for i in reg.findall(res.text):
        dict[i[0]] = i[1]
    return dict

def produceHeaders(stationUrl):
    reg=re.compile(r'^.+(\d{4}-\d{2}-\d{2}).+from_station=([A-Z]{3}).+to_station=([A-Z]{3})')
    cookies['_jc_save_fromDate']=reg.search(stationUrl).group(0)
    cookies['_jc_save_fromStation']=reg.search(stationUrl).group(1)
    cookies['_jc_save_toDate']=reg.search(stationUrl).group(0)
    cookies['_jc_save_toStation']=reg.search(stationUrl).group(2)
    headers['Cookie']=str(cookies)

def parseTrainMessage(res):
    trainMessage=[]
    for i in json.loads(res.text)['data']['result']:
        tran=OrderedDict()
        trans = i.split('|')
        tran['车次'] = trans[3]
        tran['出发时间'] = trans[8]
        tran['到达时间'] = trans[9]
        tran['历时'] = trans[10]
        tran['商务座特等座'] = trans[32] or '--'
        tran['一等座'] = trans[31] or '--'
        tran['二等座'] = trans[30] or '--'
        tran['高级软卧'] = trans[21] or '--'
        tran['软卧'] = trans[23] or '--'
        tran['动卧'] = trans[33] or '--'
        tran['硬卧'] = trans[28] or '--'
        tran['软座'] = trans[24] or '--'
        tran['硬座'] = trans[29] or '--'
        tran['无座'] = trans[26] or '--'
        trainMessage.append(tran)
    return trainMessage

def printMessage(List):
    print('=========================================================================================================')
    for i in List:
        trainMessage='车次:%s\t起始站:「%s」\t终点站:「%s」\t出发时间:%s\t到达时间:%s\t历时:%s'%(i['车次'],params['fromStation'],params['toStation'],i['出发时间'],i['到达时间'],i['历时'])
        seatMessage='商务座/特等座:「%s」 一等座:「%s」 二等座:「%s」 软卧:「%s」 动卧:「%s」 硬卧:「%s」 软座:「%s」 硬座:「%s」 无座:「%s」'%(i['商务座特等座'],i['一等座'],i['二等座'],i['软卧'],i['动卧'],i['硬卧'],i['软座'],i['硬座'],i['无座'])
        print(trainMessage)
        print(seatMessage)
        print('=========================================================================================================')


def store(List):
    df=pandas.DataFrame(List)
    df.to_excel('%s%s-%s.xlsx'%(params['date'],params['fromStation'],params['toStation']))