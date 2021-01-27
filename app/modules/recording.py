import pyaudio
import wave
import datetime
import time
import sys
import numpy as np
import utility
import pickle

st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
    dev = p.get_device_info_by_host_api_device_index(0, i)
    if (dev.get('maxInputChannels')) > 0:
        print(
            "Input Device id " + str(i) + " - " + dev.get('name') +
            ", Channels count: " + str(dev.get('maxInputChannels')) +
            ", Default sample rate: " + str(dev.get('defaultSampleRate'))
        )

try:
    input = raw_input
except NameError:
    pass

device = p.get_device_info_by_host_api_device_index(0, int(input("Chose device: ")));

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = int(device.get('maxInputChannels'))
RATE = int(device.get('defaultSampleRate'))
#RATE = 192000
INPUT_DEVICE_INDEX = int(device.get('index'))
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = st + ".wav"

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input_device_index=INPUT_DEVICE_INDEX,
                input=True,
                frames_per_buffer=CHUNK)

print("start recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK,exception_on_overflow=False)
    frames.append(data)

print(len(frames));
print("stop recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

with wave.open(WAVE_OUTPUT_FILENAME) as w:
    framerate = w.getframerate()
    frames = w.getnframes()
    channels = w.getnchannels()
    width = w.getsampwidth()
    print('sampling rate:', framerate, 'Hz')
    print('length:', frames, 'samples')
    print('channels:', channels)
    print('sample width:', width, 'bytes')

    data = w.readframes(frames)

    print(len(data))