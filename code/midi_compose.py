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

NOTE_MAX_VALUE = 12
NOTE_RANGE = np.arange(NOTE_MAX_VALUE)

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
WHITE_KEYS = [0, 2, 4, 5, 7, 9, 11]
BLACK_KEYS = [1, 3, 6, 8, 10]
NOTE_PER_OCTAVE = len(NOTE_NAMES)
NOTE_NAME_MAP_FLAT = {}
NOTE_VALUE_MAP_FLAT = {}
NOTE_NAME_MAP_SHARP = {}
NOTE_VALUE_MAP_SHARP = {}


control_number_dict = {
    """對照表
    key: value -->
    control number: control value(use funtion to control on or off)
    """
}



for idx in range(128):
    note_idx = idx % NOTE_PER_OCTAVE
    oct_idx = idx / NOTE_MAX_VALUE
    note_name = NOTE_NAMES[note_idx]

    if len(note_name) == 2:
        # 升記號
        flat = NOTE_NAMES[note_idx + 1] + 'b'
        NOTE_NAME_MAP_FLAT['%s_%d' % (flat, oct_idx)] = idx
        NOTE_NAME_MAP_SHARP['%s_%d' % (note_name, oct_idx)] = idx
        NOTE_VALUE_MAP_FLAT.append('%s_%d' % (flat, oct_idx))
        NOTE_VALUE_MAP_SHARP.append('%s_%d' % (note_name, oct_idx))
        globals()['%s_%d' % (note_name[0] + 's', oct_idx)] = idx
        globals()['%s_%d' % (flat, oct_idx)] = idx
    else:
        NOTE_NAME_MAP_FLAT['%s_%d' % (note_name, oct_idx)] = idx
        NOTE_NAME_MAP_SHARP['%s_%d' % (note_name, oct_idx)] = idx
        NOTE_VALUE_MAP_FLAT.append('%s_%d' % (note_name, oct_idx))
        NOTE_VALUE_MAP_SHARP.append('%s_%d' % (note_name, oct_idx))
        globals()['%s_%d' % (note_name, oct_idx)] = idx












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
                elif message.type == 'set_temp'
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


