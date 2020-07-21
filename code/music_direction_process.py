#-*- coding:utf-8 _*-  
""" 
@Author: John
@Email: workspace2johnwu@gmail.com
@License: Apache Licence 
@File: MusicDir_process.py 
@Created: 2020/07/16
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


import numpy as np
import glob
from os import listdir
import sys
import Music_process


np.set_printoptions(threshold=sys.maxsize)


#User info Dir
wav_dir = './music/dataset/'
user_type = input("Input the direction name in wav_dataset direction")
wav_dir += user_type +'/'

files = glob.glob('%s*.midi' %(wav_dir))
file_list = []
for file in files:
    file = file.split('.', 2)[1]
    file = '.' + file
    file_list.append(file)


music_process = Music_process(file_list)











