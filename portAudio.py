
# coding: utf-8

# In[ ]:


import pyaudio
import wave
import datetime
import time
import sys
import numpy as np
import utility

st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0);
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        dev = p.get_device_info_by_host_api_device_index(0, i);
        if (dev.get('maxInputChannels')) > 0:
            print (
                "Input Device id "+ str(i)+ " - "+ dev.get('name')+ 
                ", Channels count: "+ str(dev.get('maxInputChannels')) +
                ", Default sample rate: " + str(dev.get('defaultSampleRate'))
            )

try:
    input = raw_input
except NameError:
    pass

device = p.get_device_info_by_host_api_device_index(0, int(input("Chose device: ")));

CHUNK = 1024;
FORMAT = pyaudio.paInt24;
CHANNELS = int(device.get('maxInputChannels'));
RATE = int(device.get('defaultSampleRate'));
#RATE = 192000;
INPUT_DEVICE_INDEX = int(device.get('index'));
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = st+".wav"

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input_device_index = INPUT_DEVICE_INDEX,
                input=True,
                frames_per_buffer=CHUNK)

print("start recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
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


# In[10]:


sig = np.frombuffer(data, dtype='<i2').reshape(-1, channels)

normalized = utility.pcm2float(sig, np.float32)


# In[11]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np

plt.plot(normalized)


# In[12]:


normalized.shape


# In[13]:


import ipywidgets as widgets
from ipywidgets import interact

slider = widgets.FloatRangeSlider(value=[0,3.0],min=0.01,max=3.0,step=0.001,continuous_update=False)

def calculate_intervals(time):
    x = (1*time/RECORD_SECONDS)
    return int(frames*x)

def plot_graph(time):
    interval1 = calculate_intervals(time[0])
    interval2 = calculate_intervals(time[1])
    res = []
    for i in sig.T:
        res.append(i[interval1:interval2])
    
    plt.plot(np.array(res).T)


interact(plot_graph,time=slider);



# In[14]:


sig


# In[7]:


print(device)

