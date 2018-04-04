import requests,json
import re
if __name__=='__main__':
    url='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9050'
    res=requests.get(url)
    reg=re.compile(r'([\u4e00-\u9fa5]+)\|([A-Z]{3})')
    dict={}
    for i in reg.findall(res.text):
        dict[i[0]]=i[1]
    fromStation='北京'
    toStation='上海'
    date='2018-04-07'
    cookies={
        '_jc_save_fromDate':date,
        '_jc_save_fromStation':dict[fromStation],
        '_jc_save_toDate':date,
        '_jc_save_toStation':dict[toStation],
        '_jc_save_wfdc_flag':'dc',
        'BIGipServerotn':'317719050.64545.0000',
        'JSESSIONID':'DE445E3A0CAA6CA16BCAAE7220BD5235',
        'RAIL_DEVICEID':'sQTzWXgZi0wrqNnKZ7q6PF6r5v5l20yhqjTp05k - d6oxG5BvkPoSOBmKHYt2tYwkvuNkbZUI6X0j5eKitpfO0eWPYePxZDyrs580I - LJB_SGb3flqKmOURTQqpZ5ZvmCOLl19eohgvZoiMwiBRugSlUPvpiY3XUJ',
        'RAIL_EXPIRATION':'1523045770269',
        'route':'9036359bb8a8a461c164a04f8f50b252'
    }

    stationUrl='https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date='+date+'&leftTicketDTO.from_station='+dict[fromStation]+'&leftTicketDTO.to_station='+dict[toStation]+'&purpose_codes=ADULT'

    headers={
        'Accept':'*/*',
        'Accept-Encoding':'gzip,deflate,br',
        'Accept-Language':'en-US,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.5,zh-HK;q=0.3,en;q=0.2',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Cookie':str(cookies),
        'Host':'kyfw.12306.cn',
        'If-Modified-Since':'0',
        'Referer':'https://kyfw.12306.cn/otn/leftTicket/init',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
    }
    res=requests.get(stationUrl,headers=headers)
    res.encoding='utf-8'
    checi=[]
    for i in json.loads(res.text)['data']['result']:
        tran={}
        trans=i.split('|')
        tran['车次']=trans[3]
        tran['出发时间']=trans[8]
        tran['到达时间']=trans[9]
        tran['历时']=trans[10]
        tran['高级软卧']=trans[21] or '--'
        tran['软卧']=trans[23] or '--'
        tran['软座']=trans[24] or '--'
        tran['无座']=trans[26] or '--'
        tran['硬卧']=trans[28] or '--'
        tran['硬座']=trans[29] or '--'
        tran['二等座']=trans[30] or '--'
        tran['一等座']=trans[31] or '--'
        tran['商务座特等座']=trans[32] or '--'
        tran['动卧']=trans[33] or '--'
        info = (
        '车次:{}\t出发站:{}\t目的地:{}\t出发时间:{}\t到达时间:{}\t消耗时间:{}\n座位情况： 商务座/特等座：「{}」 一等座：「{}」 二等座：「{}」 高级软卧：「{}」 软卧：「{}」 动卧：「{}」 软卧：「{}」 硬座：「{}」 硬座：「{}」 无座：「{}」\n\n'.format(
            tran['车次'],fromStation,toStation,tran['出发时间'],tran['到达时间'],tran['历时'],
            tran['商务座特等座'],tran['一等座'],tran['二等座'],tran['高级软卧'],tran['软卧'],tran['动卧'],tran['硬卧'],tran['软座'],tran['硬座'],tran['无座']))
        print(info)