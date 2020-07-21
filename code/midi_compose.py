#-*- coding:utf-8 _*-  
""" 
@Author: John
@Email: workspace2johnwu@gmail.com
@License: Apache Licence 
@File: midi_compose.py 
@Created: 2020/07/17
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


from mido import MidiTrack, MidiFile, Message
from mido.midifiles import MetaMessage
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)


control_number_dict = {
    """對照表
    key: value -->
    control number: control value(use funtion to control on or off)
    """
}

def tickToDur(ticks, resolution = 96):
    return float(ticks) / float((resolution * 4))

def getChannal(track):
    if len(track) > 0:
        e = track[0]










def trackToEvent(note_on_lenght, ticksPerBeat=96, defaultPatch=-1):

    return


def fromMidi(file_path, res_factor=12):
    #res_factor 音訊解析度

    mid = MidiFile(file_path)
    note_time_onoff = getNoteTimeOnOffArray(mid, res_factor)
    note_on_length = getNoteOnLenghtArray(note_time_onoff)
    return note_on_length

def getNoteTimeOnOffArray(mid, res_factor):
    note_time_onoff_array = []

    for track in mid.tracks:
       current_time = 0
       for message in track:
            if not isinstance(message, MetaMessage):
                current_time += int(message.time / res_factor)
                if message.type == 'note_on':
                    note_onoff = 2
                    note_time_onoff_array.append([note_onoff, current_time, message.note])
                elif message.type == 'note_off':
                    note_onoff = 1
                    note_time_onoff_array.append([note_onoff, current_time, message.note])
                elif message.type == 'control_change':
                    note_onoff = 0
                    control_note = None
                    note_time_onoff_array.append([note_onoff, current_time, control_note,message.control])
                elif message.type == 'program_change':
                    currentPatch = message.program
                    print(currentPatch) #instrucment: right now is not used
                else:
                    print("Error: Note type not recongnized")


    return note_time_onoff_array



def getNoteOnLenghtArray(note_time_onoff_array):
    note_on_lenght_array = []
    for i, message in enumerate(note_time_onoff_array):
        if message[0] == 2:
            start_time = message[1]
            for j, event in enumerate(note_time_onoff_array[i:]):
                if (event[2] == message[2] and event[0] == 0) \
                    or (event[0] == message[0] and event[2] != message[2]):
                    #note_on 連接 note_on, note_on連接note_off
                    length = event[1] - start_time
                    break
                elif event[0] != message[0]:
                    if note_time_onoff_array[i+j+1][0] == 'control_change':
                        continue
                    else:
                        length = event[1] - start_time
                        break
            note_on_lenght_array.append([message[2], start_time, length])
    return  note_on_lenght_array


