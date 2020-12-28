
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

# Ініціалізуємо екземпляр фасада PyAudio
p = pyaudio.PyAudio()
# Дістаємо інформацію про доступну периферію
info = p.get_host_api_info_by_index(0);
# Отримуємо кількість достувних пристроїв
numdevices = info.get('deviceCount')
# Ініціалізуємо цикл обходу по всіх пристроях
for i in range(0, numdevices):
        # Отримуємо обєкт пристрою, який містить інформацію про пристрій
        dev = p.get_device_info_by_host_api_device_index(0, i);
        # Якщо пристрій має менше 1 каналу, він нас не цікавить, інакше виводимо інформацію
        if (dev.get('maxInputChannels')) > 0:
            # Фунція виводу тексту в термінал, обєднуємо данні про пристрій для його подальшого вибору
            print (
                "Input Device id "+ str(i)+ " - "+ dev.get('name')+ 
                ", Channels count: "+ str(dev.get('maxInputChannels')) +
                ", Default sample rate: " + str(dev.get('defaultSampleRate'))
            )

# Перевіряємо на помилку
try:
    #Ініціалізуємо ввід користувача в конольному інтерфейсі, та присвоюємо ідентифікатор обраного пристрою
    input = raw_input
except NameError:
    # Якщо помилка,то нічого не робимо
    pass

# Обираємо пристрій, той що ввів користувач
device = p.get_device_info_by_host_api_device_index(0, int(input("Chose device: ")));

# По скільки байт будемо считувати з буфера
CHUNK = 1024;
# Формат данних, те саме що int24, де 24 розрядність
FORMAT = pyaudio.paInt24;
# Дістаємо з пристрою кількість всіх доступних каналів
CHANNELS = int(device.get('maxInputChannels'));
# Дістаємо частоту пристрою, за замовченням, можна встановити вручну, як закоментовано нижче.
RATE = int(device.get('defaultSampleRate'));
#RATE = 192000;
# Індекс пристрою, для того щоб PyAudio розуміло з чим працювати
INPUT_DEVICE_INDEX = int(device.get('index'));
# Час зчитування у секундах
RECORD_SECONDS = 3
# Ім'я файлу(можна задати будь яке)
WAVE_OUTPUT_FILENAME = st+".wav"

# За добопогою визначених констант та змінних, створюємо потік, який звертаєтся до пристрою та зчитує данні його буферу обміну
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input_device_index = INPUT_DEVICE_INDEX,
                input=True,
                frames_per_buffer=CHUNK)

# Вивід для розуміння, що процес зчитування почався.
print("start recording")

# Ініціалізуємо структуру, де будема зберігати данні буферу обраного пристрою.
frames = []

# В залежності від частоти, кроку та кількості секунд, ініціалізуємо цикл зчитування, який буде тривати 3 секунди
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    # Присвоюєм зчитаний фрейм з обраним кроком у проміжну змінну
    data = stream.read(CHUNK)
    # Додаємо фрейм до структури фреймів.
    frames.append(data)

# Виводимо кількість фреймів
print(len(frames));
# Вивід для розуміння, що процес зчитування закінчився
print("stop recording")

# Зупиняєо процес зчитування
stream.stop_stream()
# Звільняємо память потоку
stream.close()
# Звільняємо память бібліотеки
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

