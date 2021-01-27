import wave
import datetime
import time
import os


def create_wav_record_from_buffer(frames, options):
    file_name = get_record_file_name()

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(options.CHANNELS)
    wf.setsampwidth(options.SAMPLE_WIDTH)
    wf.setframerate(options.RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return file_name


def test_creation_wav_record_from_buffer(frames, options):
    file_name = create_wav_record_from_buffer(frames, options)
    with wave.open(file_name) as w:
        frame_rate = w.getframerate()
        frames = w.getnframes()
        channels = w.getnchannels()
        width = w.getsampwidth()
        os.remove(file_name)

        return {
            'Sampling rate(Hz)': frame_rate,
            'Length(samples)': frames,
            'Channels': channels,
            'Sample width(bytes)': width
        }


def get_record_file_name():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + ".wav"
