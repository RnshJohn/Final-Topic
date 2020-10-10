#-*- coding:utf-8 _*-
"""
@Author: John
@Email: workspace2johnwu@gmail.com
@License: Apache Licence
@File: midi_compose.py
@Created: 2020/08/22
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


import dlib
import imutils
import cv2
import time
import threading
import numpy as np
from time import sleep
import face_recognition as fr
import shutil
import os
import tkinter
import time


class camCapture(object):
    def __init__(self, is_write=False, URL=None, save_path=None):
        """
        to init the param
        :param is_write: boolean, to check user prefer write or not
        :param URL: str, input the camera's or video address
        :param save_path: default write path is demo.avi, and it is customize
        """

        self.save_path = save_path
        self.writer = None
        self.URL = URL
        self.Frame = []
        self.status = False
        self.isstop = False
        self.dir_index = 0
        self.is_write = is_write
        self.write_num = 0


        if URL is None:
            self.capture = cv2.VideoCapture(1)

        else:
            self.capture = cv2.VideoCapture(URL)

        status, frame = self.capture.read()
        print(status, frame)





    def sub_thread_start(self):
        """
        to use the threading method make multiprograming
        :return: None
        """

        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def sub_thread_stop(self):
        """
        to check the streaming is stop
        :return: None
        """

        self.isstop = True
        print('StreamStop')

    def get_frame(self):
        """
        :return: frame
        """
        return self.Frame

    def queryframe(self):
        """
        to
        :return:
        """

        self.size = (int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                     int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print(self.size)

        if self.is_write:
            fourcc = cv2.VideoWriter_fourcc(*'divx')

            if self.save_path is None:
                save_path = 'demo.avi'

            self.writer = cv2.VideoWriter(self.save_path, fourcc, 40, self.size)


        frame_count = 0
        FPS= "0"
        detector = dlib.get_frontal_face_detector()

        while not self.isstop:

            status, frame = self.capture.read()
            print(status, frame)

            if status:
                # #count 10 frame's FPS
                # blurred = np.hstack([cv2.GaussianBlur(self.Frame, (3, 3), 0),
                #                      cv2.GaussianBlur(self.Frame, (5, 5), 0),
                #                      cv2.GaussianBlur(self.Frame, (7, 7), 0)])
                # diff = cv2.absdiff(blurred_avg, blurred)
                #
                # #將圖片轉為灰階
                # gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                # ret, tresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
                #
                # #使用型態轉換函數去除雜訊
                # kernel = np.ones((5, 5), np.uint8)
                # thresh = cv2.morphologyEx(tresh, cv2.MORPH_OPEN, )


                if frame_count == 0:
                    t_start=  time.time()
                frame_count += 1
                if frame_count >= 60:
                    FPS = "FPS=%1f" % (60 / (time.time() - t_start))
                    frame_count = 0
                    self.img_process(detector, frame, self.writer)
                    self.dir_index += 1



                if self.writer is not None:
                    self.writer.write(self.Frame)


                #確認temp_dic is full
                if self.dir_index >= 50:
                    self.clear_diction_data()
                    self.dir_index = 0


                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print('get image false')
                break



        self.capture.release()

        if self.writer is not None:
            self.writer.release()




    def img_process(self, detector, frame, writer):

        current_time = time.strftime('%Y%m%d%H%M%S')
        face_react, scores, idx = detector.run(frame, 0)
        for i, d in enumerate(face_react):
            x1 = d.left()
            y1 = d.top()
            x2 = d.right()
            y2 = d.bottom()

            text = "%2.2f(%d)" % (scores[i], idx[i])

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4, cv2.LINE_AA)

            #face detector 臉部截截取
            face_img = frame[y1: y2, x1: x2]
            temp_time = current_time+'_'+str(i+1)
            face_path = "./face/{}.jpg".format(temp_time)
            cv2.imwrite(face_path, face_img)

            cv2.putText(frame, text, (x1, y1), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

        write_path = './temp_data/{}.jpg'.format(current_time)
        cv2.imwrite(write_path, frame)
        cv2.imshow("Face Dectection", frame)



    def clear_diction_data(self):
        shutil.rmtree('./temp_data')
        os.makedirs('./temp_data')






# class MyThread(threading.Thread):
#     def __init__(self, ):
#         threading.Thread.__init__(self)
#
#     def run(self):



