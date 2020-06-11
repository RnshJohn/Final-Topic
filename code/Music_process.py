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


np.set_printoptions(threshold=sys.maxsize ,precision=4)


class MusicProcess(object):
    """MusicProcess Class

    Parameters
    ----------

    """

    def __init__(self, wavFilename):

        self.xls_file = 'wave.data'
        self.wavFilename = wavFilename

    def interface(self):
        """User interface
        To interact with all methods.

        Parameters
        ----------
        None

        Return
        ------

        """


        #Process the file header  example: piano101.wav process after is string: piano
        wavfile_header = os.path.splitext(self.wavFilename)[0]
        # format = '1234567890'
        # for unit in file_header:
        #     if  unit in format:
        #         file_header = file_header.replace(unit ,'')
        reset_wavfile_header = filter(str.isalpha, wavfile_header)
        reset_wavfile_header = ''.join(reset_wavfile_header)

        # if reset_file_header in self._instructments:
        #     self.wav_transform2data()
        #
        # else:
        #     self.add_sheet(reset_file_header)

        wave_data = self.wav_transform2data(self.wavFilename)
        self.search_instructments(wave_data, sheetName = reset_wavfile_header)







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
            table = [[c.value for c in sheet.row(i)] for i in range(sheet.nrows)]
            np.vstack((table, data))






        except IOError:
            sys.stdout.write('No such file: %s\n' % self.xls_file)
        sys.stdout.flush()



    def wav_transform2data(self, filename):
        """"""
        sampling_freq, audio = wavfile.read(self.filename)
        audio =  audio / np.max(audio)
        self.fft_signal = np.fft.fft(audio)
        self.fft_signal = abs(self.fft_signal)
        self.Freq = np.arange(0, len(self.fft_signal))





        return self




    def write_xls(self):
        """"""
        workbook = xlwt.Workbook(encoding='utf8')

    def add_sheet(self, sheetname):
        """"""









