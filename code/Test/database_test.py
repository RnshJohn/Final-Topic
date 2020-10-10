# -*- coding:utf-8 _*-
""" 
@Author: John
@Email: workspace2johnwu@gmail.com
@License: Apache Licence 
@File: database_test.py 
@Created: 2020/09/16
@site:  
@software: PyCharm 

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃            ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神獸保佑    ┣┓
                ┃　永無BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛ 
"""

import mysql.connector
import os
import sys
from PIL import Image
from connect import *
import time
import hashlib




conn = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "851411asd",
    database = "userdb",
)
cursor = conn.cursor()
# cursor.execute("CREATE TABLE users(name VARCHAR(255), phone_number INTEGER(20), email VARCHAR (99),Data MEDIUMBLOB,user_id INTEGER  AUTO_INCREMENT PRIMARY KEY );")



#read img path

# path =
# try:
#     fin = open(path)
#     img = fin.read(fin)
#     fin.close()



def md5(arg):
    md5_pwd=hashlib.md5(bytes('abd',encoding='utf-8'))
    md5_pwd.update(bytes(arg,encoding='utf-8'))
    return md5_pwd.hexdigest()




def register():
    try:
        while True:
            name=input("輸入你的名字:").strip()
            cursor.execute("selectcount(*)fromuserwherename=%s",name)
            count=cursor.fetchone()[0]
            length=len(name)
            if count==1:
                print("使用者名稱已存在!")
                continue
            elif length<6:
                print("使用者名稱最少6個字元!")
                continue
            elif length>15:
                print("使用者名稱最多15個字元!")
                continue
            elif count == 0 and length >= 6 and length <= 15:
                password=input("輸入你的密碼:").strip()
                time=int(time.time())
                string=name+password+str(time)
                passwd=md5(string)
                cursor.execute("insertintouser(name,passwd,createtime)values(%s,%s,%s)",(name,passwd,time))
                break
    except:
        conn.rollback()
    else:
        conn.commit()
        conn.close()
