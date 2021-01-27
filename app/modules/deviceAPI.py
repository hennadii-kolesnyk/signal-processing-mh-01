from pyaudio import PyAudio


class DeviceApi:

    def __init__(self, p: PyAudio):
        self.py_audio = p

    def get_available_devices(self):
        info = self.py_audio.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        devices = []
        for i in range(0, num_devices):
            device = self.py_audio.get_device_info_by_host_api_device_index(0, i)
            if (device.get('maxInputChannels')) > 0:
                devices.append(device)
        return devices

    def get_device_by_index(self, index: int):
        return self.py_audio.get_device_info_by_host_api_device_index(0, index)

    def validate_devices(self, device1, device2):
        return True

