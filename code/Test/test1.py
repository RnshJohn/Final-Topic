#-*- coding:utf-8 _*-  
""" 
@Author: John
@Email: workspace2johnwu@gmail.com
@License: Apache Licence 
@File: test1.py 
@Created: 2020/07/06
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


import sys
import wave
import numpy as np
import matplotlib.pyplot as plt


np.set_printoptions(threshold=sys.maxsize, precision=4)



audio_path = '../music/piano.wav'

wave_read = wave.open(audio_path, 'rb')


params = wave_read.getparams()

nchannels, sampwidth, framerate, nframes = params[:4]

wave_time = np.arange(0, nframes) / framerate


str_data = wave_read.readframes(nframes)

wave_read.close()

wave_data = np.fromstring(str_data, dtype=np.short)

wave_data = np.reshape(wave_data, [nframes, nchannels])


plt.plot(wave_time, wave_data[:])
plt.show()



for i in range(wave_data.shape[0]):
    wave_data[i, :] = wave_data[i, :] - np.mean(wave_data[i, :])


plt.plot(wave_time, wave_data[:])
plt.show()





