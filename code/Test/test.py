import abc
import bunch
import contextlib
import collections
import warnings
import librosa
import matplotlib.pyplot as plt
import librosa.display
import wave
import json
import numpy as np
import sys
from scipy.io import wavfile
from scipy.io.wavfile import write
from sklearn.preprocessing import StandardScaler
import scipy.signal as signal
import struct
import contextlib

np.set_printoptions(threshold=sys.maxsize, precision=4)


audio_path = '../music/piano.wav'
x, sr = librosa.load(audio_path, sr=None)
print(type(x), type(sr))
plt.figure(figsize=(14, 5))
librosa.display.waveplot(x, sr=sr)
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.show()


Wave_read = wave.open('../music/piano.wav', 'rb')
params = Wave_read.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]

str_data = Wave_read.readframes(nframes)
Wave_read.close()

wave_data = np.fromstring(str_data, dtype=np.short)
# wave_data = wave_data*1.0/(max(abs(wave_data)))
wave_data = np.reshape(wave_data, [nframes, nchannels])
time = np.arange(0, nframes) * (1.0 / framerate)

plt.figure()

plt.subplot(2, 1, 1)
plt.plot(time, wave_data[:, 0])
plt.xlabel('time (seconds)')
plt.ylabel('Amplititude')
plt.title('Left channel')
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(time, wave_data[:, 1], c='g')
plt.xlabel('time(seconds)')
plt.ylabel('Amplitude')
plt.title('Right channel')
plt.grid()

#
# plt.show()
#
#
#
# # 弗利葉轉換
sampling_freq, audio = wavfile.read(r'../music/piano.wav')
#
# sc = StandardScaler()
#
#
audio = audio / np.max(audio)
# audio = sc.fit_transform(audio)

fft_signal = np.fft.fft(audio)

fft_signal = abs(fft_signal)
Freq = np.arange(0, len(fft_signal))
#
plt.figure()
plt.plot(Freq, fft_signal, color='blue')
plt.xlabel('Freq (in kHz)')
plt.ylabel('Amplitude')
plt.show()



framerate = 44100
time = 10

t = np.arange(0, time, 1.0/framerate)

wave_data = signal.chirp(t, 100, time, 1000, method='linear')

wave_data = wave_data.astype(np.short)

f = wave.open(r'sweep.wav', 'wb')
f.setnchannels(1)
f.setsampwidth(2)
f.setframerate(framerate)
comptype = 'None'
compname = 'not compressed'

f.writeframes(wave_data.tostring())
f.close()



with wave.open(r'./piano.wav')as f:
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)
    waveData = np.fromstring(strData, dtype=np.short)

waveData = waveData * 1.0 / max(abs(waveData))

outData = waveData

with wave.open(r'write.wave', 'wb') as outwave:
    nchannels = 1
    sampwidth = 2
    framerate = 8000
    nframes = len(outData)

    comtype = 'NONE'
    compname = 'not compressed'
    outwave.setparams((nchannels, sampwidth, framerate, nframes,
                       comtype, compname))

    for i in outData:
        outwave.writeframes(struct.pack('h', int(i * 64000 / 2)))


output_file = 'output_generated.wave'
duration = 3
sampling_freq = 44100
tone_freq = 587
min_val = -2 * np.pi
max_val = 2 * np.pi

t = np.linspace(min_val, max_val, duration * sampling_freq)
audio = np.sin(2 * np.pi * tone_freq * t)

noise = 0.4 * np.random.rand(duration * sampling_freq)
audio += noise

scaling_factor = pow(2, 15) -1
audio_normalized = audio / np.max(np.abs(audio))
audio_scaled = np.int16(audio_normalized * scaling_factor)
write(output_file, sampling_freq, audio_scaled)


audio = audio[: 300]
x_values = np.arange(0, len(audio), 1) / float(sampling_freq)
x_values *= 1000 #轉換微秒
plt.plot(x_values, audio, color='blue')
plt.xlabel('Time(ms)')
plt.ylabel('Amplitude')
plt.title('Audio signal')
plt.show()


def Synthetic_tone(freq, duration, amp=1.0, sampling_freq=44100):
    t = np.linspace(0, duration, duration * sampling_freq)
    audio = amp * np.sin(2 * np.pi * freq * t)
    return audio.astype(np.int16)

tone_map_file = 'tone_freq_map.json'

with open(tone_map_file, 'r') as f:
    tone_freq_map = json.loads(f)
    print(tone_freq_map)

input_tone = 'G'
duration = 2
amplitude = 10000
sampling_freq = 44100


synthesized_tone = Synthetic_tone(tone_freq_map[input_tone], duration, amplitude, sampling_freq)
write('output_tone.wave', sampling_freq, synthesized_tone)


tone_seq = [('D', 0.3), ('G', 0.6), ('C', 0.5), ('A', 0.3), ('Asharp', 0.7)]



output = np.array([])
for item in tone_seq:
    input_tone = item[0]
    duration = item[1]
    synthesized_tone = Synthetic_tone(tone_freq_map[input_tone], duration, amplitude, sampling_freq)
    output.append(output, synthesized_tone, axis=0)

write('output_tone_seq.wav', sampling_freq, output)










# def meth():
#     print("Calling method")
#
#
# class MyMeta(type):
#     @classmethod
#     def __prepare__(cls, name, baseClasses):
#         return {'meth': meth}
#
#     def __new__(cls, name, baseClasses, classdict):
#         return type.__new__(cls, name, baseClasses, classdict)
#
#
# class Test(metaclass=MyMeta):
#     def __init__(self):
#         pass
#
#     attr = 'an attribute'
#
#
# t = Test()
# print(t.attr)

#
# class SimpleBunch(object):
#     def __init__(self, **fields):
#         self.__dict__ = fields
#
#
# class Point(bunch.Bunch):
#     x = 1.0
#     y = 0.0
#     color = 'gray'


# class MetaBunch(type):
#     def __prepare__(name, *bases, **kwargs):
#         return collections.OrderedDict()
#
#     def __new__(mcl, classname, bases, classdicts):
#         def __init__(self, **kw):
#             for k in self.__dflts__:
#                 setattr(self, k, self.__dflts__[k])
#
#             for k in kw:
#                 setattr(self, k, kw[k])
#
#         def __repr__(self):
#             repr = ['{}={!r}'.format(k, getattr(self, k))
#                     for k in self.__dflts__
#                     if getattr(self, k) != self.__dflts__[k]
#                     ]
#
#
#
#
# @contextlib.contextmanager
# def tag(tagname):
#     print('{}'.format(tagname))
#     try:
#         yield
#     finally:
#         print("</{}>".format(tagname))
#
# tt = tag('sometage')
#
# with tt:
#     print("hello")
#
#
#
#
#


import logging
import sys
import traceback
import datetime
import wx


## @detail 创建记录异常的信息
# class ExceptHookHandler(object):
#     ## @detail 构造函数
#     #  @param logFile: log的输入地址
#     #  @param mainFrame: 是否需要在主窗口中弹出提醒
#     def __init__(self, logFile, mainFrame=None):
#         self.__LogFile = logFile
#         self.__MainFrame = mainFrame
#
#         self.__Logger = self.__BuildLogger()
#         # 重定向异常捕获
#         sys.excepthook = self.__HandleException
#
#     ## @detail 创建logger类
#     def __BuildLogger(self):
#         logger = logging.getLogger()
#         logger.setLevel(logging.DEBUG)
#         logger.addHandler(logging.FileHandler(self.__LogFile))
#         return logger
#
#     ## @detail 捕获及输出异常类
#     #  @param excType: 异常类型
#     #  @param excValue: 异常对象
#     #  @param tb: 异常的trace back
#     def __HandleException(self, excType, excValue, tb):
#         # first logger
#         try:
#             currentTime = datetime.datetime.now()
#             self.__Logger.info('Timestamp: %s' % (currentTime.strftime("%Y-%m-%d %H:%M:%S")))
#             self.__Logger.error("Uncaught exception：", exc_info=(excType, excValue, tb))
#             self.__Logger.info('\n')
#         except:
#             pass
#
#         # then call the default handler
#         sys.__excepthook__(excType, excValue, tb)
#
#         err_msg = ''.join(traceback.format_exception(excType, excValue, tb))
#         err_msg += '\n Your App happen an exception, please contact administration.'
#         # Here collecting traceback and some log files to be sent for debugging.
#         # But also possible to handle the error and continue working.
#         dlg = wx.MessageDialog(None, err_msg, 'Administration', wx.OK | wx.ICON_ERROR)
#         dlg.ShowModal()
#         dlg.Destroy()





# def create_btree(tree, data):
#     for i in range(len(data)):
#         level = 0
#         if i == 0:
#            tree[level] == data[i]
#         else:
#             while tree[level]:
#                 if data[i] > tree[level]:
#                     level = level * 2 + 2
#                 else:
#                     level = level * 2 + 1
#         tree[level] = data[i]
#
#
# class Node():
#     def __init__(self, data=None):
#         self.data = data
#         self.left = None
#         self.right = None
#     def insert(self, data):
#         if self.data:
#             if data < self.data:
#                 if self.left:
#                     self.left.insert(data)
#                 else:
#                     self.left = Node(data)
#             else:
#                 if self.right:
#                     self.right.insert(data)
#                 else:
#                     self.right = Node(data)
#         else:
#             self.data = data
#
#     def inorder(self):
#         if self.left:
#             self.left.inorder()
#         print(self.data)
#
#         if self.right:
#             self.right.inorder()
#
#     def preordor(self):
#         print(self.data)
#         if self.left:
#             self.left.preorder()
#         if self.right:
#             self.right.preorder()
#
#     def postorder(self):
#         if self.left:
#             self.left.postorder()
#         if self.right:
#             self.right.postorder()
#         print(self.data)
#
#     def search(self, val):
#         if val < self.data:
#             if not self.left:
#                 return str(val) + "不存在"
#             return self.left.search(val)
#         elif val > self.data:
#             if not self.data:
#                 return str(val) + "不存在"
#             return self.right.search(val)
#         else:
#             return str(val) + "找到了"
#
#
# class Delete_Node():
#     def delete_node(self, root ,key):
#         if root is None:
#             return None
#         if key < root.data:
#             root.left = self.delete_node(root.left, key)
#             return root
#         if key > root.data:
#             root.right = self.delete_node(root.right, key)
#         if root.left is None:
#             new_root = root.right
#             return new_root
#         if root.right is None:
#             new_root = root.left
#             return new_root
#         succ = self.max_node(root.left)
#         tmp = Node(succ.data)
#         tmp.left = self.left_node(root.left)
#         tmp.right = root.right
#         return tmp
#     def left_node(self, node):
#         if node.right is None:
#             new_root = node.left
#             return new_root
#         node.right = self.left_node(node.right)
#         return node
#     def max_node(self, node):
#         while node.right:
#             node = node.right
#         return node
    




# tree = Node()
# datas = [10, 21, 5, 9, 13, 28]
# for d in datas:
#     tree.insert(d)
# tree.inorder()
#
#
# import heapq
# h = [10, 21, 5, 9, 13, 28, 3]
# heapq.heapify(h)
# print('堆入前和取出前 h= ')
# val = heapq.heappushpop(h, 11)
# print('取出元素',val)
# print("堆入和取出後", h)
#
#
# h = [10, 21, 5, 9, 13, 28, 3]
# print("最大三個：", heapq.nlargest(3, h))
# print("最小三個：", heapq.nsmallest(3, h))
#
#
# h = [10, 21, 5, 9, 13, 28, 3]
# heapq.heapify(h)
# print("執行前：")
#
# x = heapq.heapreplace(h, 7)
# print("取出後", x)
# print("執行後", h)







