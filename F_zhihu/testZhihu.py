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
    # print(r.scard('proxy'))
    # A=r.srandmember('proxy')
    # print(A)
    # print(r.scard('proxy'))
    r.flushdb()
