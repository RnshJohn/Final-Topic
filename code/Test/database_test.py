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

topic_db = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "851411asd",
    database = "userdb",
)
cursor = topic_db.cursor()
cursor.execute("CREATE TABLE users(name VARCHAR(255), phone_number INTEGER(20), email VARCHAR (99),img MEDIUMBLOG,user_id INTEGER  AUTO_INCREMENT PRIMARY KEY )")