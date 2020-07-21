#-*- coding:utf-8 _*-  
""" 
@Author: John

@Email: workspace2johnwu@gmail.com

@License: Apache Licence

@File: Music_process.py 

@Created: 2020/06/10

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



import os
import numpy as np
from tqdm import tqdm, trange
from time import sleep
import wave
import sys
import abc
import xlrd
import xlwt
import json
from scipy.io import wavfile
from xlrd.biffh import XLRDError
from xlutils.copy import copy
from sklearn.preprocessing import StandardScaler
import data_compose


np.set_printoptions(threshold=sys.maxsize ,precision=4)


class MusicProcess(object):
    """MusicProcess Class

    Parameters
    ----------

    """

    def __init__(self, filename_dir, instructment = 'Piano'):

        self.xls_file = 'wave.data'
        self.filename_dir = filename_dir
        self.sheetname = instructment

    def interface(self):
        """User interface
        To interact with all methods.

        Parameters
        ----------
        None

        Return
        ------

        """

        for filePath in self.filename_dir:
            #Process the file header  example: piano101.wav process after is string: piano

            # reset_wavfile_header = filter(str.isalpha, wavfile_header)
            # reset_wavfile_header = ''.join(reset_wavfile_header)
            # if reset_file_header in self._instructments:
            #     self.wav_transform2data()
            #
            # else:
            #     self.add_sheet(reset_file_header)
            self.wav_process(filePath+'.wav')
            self.midi_process(filePath+'.midi')



    def wav_process(self, filename):
        wave.open(filename, 'rb')
    def midi_process(self, filename):


    def search_instructments(self, data, sheetName=None, return_table=True):
        """

        Parameters
        ----------
        data:
        sheetName:
        return_table:

        Return
        ----------
        :param data:
        :param sheetName:
        :param return_table:
        """
        try:
            rexcel = xlrd.open_workbook(self.xls_file, on_demand=True)
            rows = rexcel.sheet_by_name("sheetName").nrows
            excel = copy(rexcel)
            try:
                sheet = excel.get_sheet("sheetName")
            except Exception:
                sheetlen = rexcel.nsheets
                sheet = excel.add_sheet("sheetName")
            # table = [[c.value for c in sheet.row(i)] for i in range(sheet.nrows)]
            # np.vstack((table, data))

            for i, row in enumerate(data):
                for j, col in enumerate(row):
                    sheet.write(i+rows, j, col)
            excel.save(self.xls_file)






        except IOError:
            sys.stdout.write('No such file: %s\n' % self.xls_file)
        sys.stdout.flush()



    def wav_transform2data(self, filename):
        """"""
        sampling_freq, audio = wavfile.read(self.wavFilename)
        audio =  audio / np.max(audio)
        self.fft_signal = np.fft.fft(audio)
        self.fft_signal = abs(self.fft_signal)
        self.Freq = np.arange(0, len(self.fft_signal))





        return self




    def write_xls(self):
        """"""
        workbook = xlwt.Workbook(encoding='utf8')











