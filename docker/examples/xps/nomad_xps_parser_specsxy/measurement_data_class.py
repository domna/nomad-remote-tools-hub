# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 08:25:00 2021

@author: Mark
"""

class MetaData:
    def __init__(self):
        self.timestamp = ''
        self.dwell_time = ''
        self.n_scans = ''
        self.excitation_energy = ''
        self.method_type = ''
        self.data_labels = []
        self.device_settings = []
        self.spectrum_region = ''
        self.source_label = ''
        self.primary_channel_id = 1
        self.axis_id = 0
        self.group_name = ''

class DeviceSettings():
    def __init__(self):
        self.device_name = ''
        self.channel_id = ''
            
class AnalyzerSettings(DeviceSettings):
    def __init__(self):
        super().__init__()
        self.pass_energy = ''
        self.lens_modes = ''
        self.detector_voltage = ''
    
class DataChannel:
    def __init__(self):   
        pass
        
class MeasurementData:
    def __init__(self):
        self.metadata = MetaData()
        self.data = []
        
    def addDataChannel(self, data_channel):
        self.data += [data_channel]
        
    def appendDataChannel(self, data_channel):
        channel_id = len(self.data)
        self.metadata.data_labels += [{'channel_id':channel_id,
                                       'label':data_channel['label'],
                                       'unit':data_channel['unit']}
                                      ]
        if 'device_settings' in data_channel.keys():
            device_settings = data_channel['device_settings']
            if not isinstance(device_settings, DeviceSettings):
                print('The device settings should be an instance of DeviceSettings')
        else:
            device_settings = DeviceSettings()
            device_settings.device_name = 'unknown device'
        device_settings.channel_id = channel_id
        self.metadata.device_settings += [device_settings]
        self.data += [data_channel['data']]
        
            

        
        
       