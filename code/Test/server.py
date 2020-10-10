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
import threading
import time
import numpy as np

def tcp_client_sent_video(TCP_PORT):

    capture = cv2.VideoCapture(1)
    host_addr = ("192.168.()", TCP_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(host_addr)
    sock.listen(True)


    client_conn, client_addr = sock.accept()
    status, frame = capture.read()


    while status:
        result, enc = cv2.imencode('.jpg', frame)
        localtime = time.asctime(time.localtime(time.time()))

        data = np.array(enc)
        strData = data.tostring()

        client_conn.send(str(len(strData)).ljust())
        client_conn.senf(strData)


        status, frame = capture.read()
        decimg = cv2.imdecode(data, 1)
        cv2.imshow('server', decimg)
        cv2.waitKey()
    client_conn.close()
    cv2.destroyAllWindows()







def tcp_client_sent_data(TCP_PORT, data):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    host_addr = ("192.168.()", TCP_PORT)

    # 綁定
    sock.bind(host_addr)
    sock.listen(128)

    # 如果有新的客户端來鏈接服務器，那麼就產生一個新的套接字專門為這個客户端服務
    client_socket, clientAddr = sock.accept()

    # 接收對方發送過來的數據
    recv_data = client_socket.recv(1024)
    print('接收到的數據為:', recv_data.decode('gbk'))

    # 發送一些數據到客户端
    client_socket.send("thank you !".encode('gbk'))

    # 關閉為這個客户端服務的套接字，只要關閉了，就意味着為不能再為這個客户端服務了，如果還需要服務，只能再次重新連接
    client_socket.close()