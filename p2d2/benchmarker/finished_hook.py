"""
A hook module should implement the fire(*args, **kwargs) interface
"""
import urllib.request

def fire(*args, **kwargs):
    print("benchmarker finished")
    url = "https://maker.ifttt.com/trigger/benchmarker_finished/with/key/bIleIB1ksFBJAlRQo5xedS41TepQ59enwButksyl8A7"
    urllib.request.urlopen(url)

