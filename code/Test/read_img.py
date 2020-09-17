#-*- coding:utf-8 _*-  
""" 
@Author: John
@Email: workspace2johnwu@gmail.com
@License: Apache Licence 
@File: read_img.py 
@Created: 2020/09/17
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


import tkinter as tk
from tkinter import filedialog
import sys

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

try:
    fin = open(file_path)
    img = fin.read()
    fin.close()
except IOError as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)

