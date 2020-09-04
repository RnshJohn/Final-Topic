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
import warnings
import struct

np.set_printoptions(threshold=sys.maxsize)

NOTE_MAX_VALUE = 12
NOTE_RANGE = np.arange(NOTE_MAX_VALUE)

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
WHITE_KEYS = [0, 2, 4, 5, 7, 9, 11]
BLACK_KEYS = [1, 3, 6, 8, 10]
NOTE_PER_OCTAVE = len(NOTE_NAMES)
NOTE_NAME_MAP_FLAT = {}
NOTE_VALUE_MAP_FLAT = []
NOTE_NAME_MAP_SHARP = {}
NOTE_VALUE_MAP_SHARP = []


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

BEAT_NAMES = ['whole', 'half', 'quarter', 'eighth', 'sixteeth', 'thirty-second', 'sixty-fourth']
BEAT_VSLUES = [4, 2, 1, .5, .25, .125, .0625]


# to ensure python2/3
if sys.version_info[0] == 3:
    int2byte = struct.Struct(">B").pack



class Event(object):
    name = 'Generic MIDI Event'
    length = 0
    status_msg = 0x0
    sort = 0.

    def __init__(self, **kwargs):
        if isinstance(self.length, int):
            data = [0] * self.length
        else:
            data = []
        self.tick = 0
        self.data = data
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __eq__(self, other):
        return (
            self.tick == other.tick and self.data == other.data and
            self.status_msg == other.status_msg
        )

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if self.tick < other.tick:
            return True
        elif self.tick == other.tick and self.sort < other.sort:
            return True
        return False

    def __le__(self, other):
        return  NotImplementedError

    def __gt__(self, other):
        if self.tick > other.tick:
            return True
        elif self.tick == other.tick and self.sort > other.sort:
            return True
        return False

    def __ge__(self, other):
        return NotImplementedError

    def __str__(self):
        return "%s: ticks: %s data: %s" % (self.__class__.__name__, self.tick, self.data)









class MetaEvent(Event):
    status_msg = 0xFF






class MIDIFile(object):
    def __init__(self, tracks=None, resolution=12, file_format=0):
        if tracks is None:
            self.tracks = []
        elif isinstance(tracks, MidiTrack):
            self.tracks = [tracks]
        elif isinstance(tracks, list):
            for track in tracks:
                if isinstance(track, MidiTrack):
                    self.tracks.append(track)
        else:
            raise ValueError('')

        self.resolution = resolution


        if  file_format > 1:
            raise ValueError('MIDI file formats 0 and 1 supported.')
        self.format = file_format


    @property
    def ticks_per_quater_note(self):
        return  self.resolution

    def tempi(self, suppress_warnings=False):
        if not suppress_warnings:
            warnings.warn('this method will be removed soon, do not rely on')

        tempo_events = []
        for i, track in enumerate(self.tracks):
            track_tempo_events = [e for e in track.events if isinstance(e, SetTempoEvent)]









def fromMidi(file_path):
    # res_factor 音訊解析度

    mid = MidiFile(file_path)
    note_time_onoff = getNoteTimeOnOffArray(mid, res_factor=12)
    note_on_length = getNoteOnLenghtArray(note_time_onoff)
    note_name_length = labelByNoteName(note_on_length)
    note_on_timeline = editTimeLine(note_name_length)
    return note_name_length

def trackToEvent(note_on_lenght, ticksPerBeat=96, defaultPatch=-1):

    return





def labelByNoteName(note_on_length):
    note_name_length = []
    for detail in note_on_length:
        for note, number in NOTE_NAME_MAP_FLAT.items():
            if detail[0] == number:
                note_name_length.append([note, detail[0], detail[1], detail[2]])


    return note_name_length


def getNoteTimeOnOffArray(mid, res_factor):
    note_time_onoff_array = []

    for track in mid.tracks:
        current_time = 0
        for message in track:
            if not isinstance(message, MetaMessage):
                current_time += int(message.time / res_factor)
                if message.type == 'note_on' and message.velocity > 0:
                    note_onoff = 2
                    note_time_onoff_array.append([note_onoff, current_time, message.note])
                elif message.type == 'note_off' or (message.type == 'note_on' and message.velocity == 0):
                    note_onoff = 1
                    note_time_onoff_array.append([note_onoff, current_time, message.note])
                elif message.type == 'control_change':
                    note_onoff = 0
                    control_note = None
                    note_time_onoff_array.append([note_onoff, current_time, control_note, message.control])
                elif message.type == 'program_change':
                    currentPatch = message.program
                    print(currentPatch)  # instrucment: right now is not used
                elif message.type == 'msg':
                    #need to handle this later
                    pass
                else:
                    print("Error: Note type not recongnized")

    return note_time_onoff_array

def getNoteOnLenghtArray(note_time_onoff_array):
    note_on_lenght_array = []
    for i, message in enumerate(note_time_onoff_array):
        if message[0] == 2:
            start_time = message[1]
            for j, event in enumerate(note_time_onoff_array[i:]):
                if (event[2] == message[2] and event[0] == 1) :
                    # note_on 連接 note_on, note_on連接note_off
                    length = event[1] - start_time
                    break
                elif event[0] == 'control_change':
                    if note_time_onoff_array[i + j + 1][0] == 'control_change':
                        continue
                    else:
                        length = event[1] - start_time
                        break
            note_on_lenght_array.append([message[2], start_time, length])
    return note_on_lenght_array




def editTimeLine(note_name_length):
    for i, note_event in enumerate(note_name_length):
        time_range = np.arange(note_event[2], note_event[2] + note_event[3] + 1)
        start_time = note_event[2]
        temp_note = [[note_event[0]]]
        temp_time_range = []
        end_time = 0
        for j, event in enumerate(note_name_length[i+1]):
            if event[2] in time_range:
                temp_note.append([temp_note[j] + event[0]])
                temp_time_range.append([start_time, event[2]])
                start_time = event[2]
                if (event[2] + event[3]) in time_range:
                    #結尾結束在range
                    temp_time_range.append([start_time, event[2] + event[3]])
                    end_time = event[2] + event[3]
                    temp_note.append([temp_note[j].pop()])
                    temp_time_range.append([end_time, note_event[2] + note_event[3]])
                else:
                    #不再range里
                    temp_time_range.append([start_time, note_event[2] + note_event[3]])
            else:

                break

        for i in len(temp_note):






