# import mysql.connector
#
#
# if __name__=='__main__':
#     conn = mysql.connector.connect(user='root',password='0202508',database='test59')
#     cursor = conn.cursor()
#     cursor.execute('select * from TEACHER;')
#     # values=cursor.fetchall()
#     # print(values)
#     for i in cursor:
#         print(i)
#     print(cursor.rowcount)
#     conn.commit()
#     cursor.close()
#     conn.close()

import redis
if __name__=='__main__':
    pool=redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)
    r=redis.Redis(connection_pool=pool)
    # r.sadd('newID','xglacier')
    print(r.scard('newID'))
    print(r.scard('oldID'))
    print(r.scard('proxy'))
    r.delete('oldID')
    print(r.scard('oldID'))
    # r.sunionstore('newID','oldID','newID')
    # r.delete('oldID')
#     # A=r.srandmember('proxy')
#     # print(A)
#     # print(r.scard('proxy'))
#     # r.flushdb()

# import requests,json,random
# from F_zhihu import Setting
# from F_zhihu import Parser
# url='https://www.zhihu.com/api/v4/members/{id}?include=name,url_token,educations,business,locations,employments,gender,following_count,follower_count,voteup_count,thanked_count,favorited_count,answer_count,articles_count,question_count.topics'
# id=['ma-wen-cai-52-25','tang-wu-92','yi-shu-ying','liu-wen-jing-53-83']
# for i in id:
#     res=requests.get(url.format(id=i),
#              proxies={'proxy': 'http://121.231.2.88:49283'},
#              headers={'User-Agent': random.choice(Setting.UA), 'Cookie': random.choice(Setting.Cookies)},
#              )
#     yep=Parser.Json(res.text)
#     yep.parseMessage()