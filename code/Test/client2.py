
#-*- coding:utf-8 _*-
"""
@Author: John
@Email: workspace2johnwu@gmail.com
@License: Apache Licence
@File: server.py.py
@Created: 2020/10/07
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


import socket
import cv2
import numpy

import socket
import cv2
import numpy

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_IP = "127.0.0.1"
TCP_PORT = 8000

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

while True:
    length = recvall(sock,16)
    stringData = recvall(sock, int(length))
    data = numpy.fromstring(stringData, dtype='uint8')
    decimg=cv2.imdecode(data,1)
    cv2.imshow('CLIENT2',decimg)
    cv2.waitKey(1)

sock.close()
cv2.destroyAllWindows()