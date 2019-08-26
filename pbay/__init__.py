import sys
import time
from collections import OrderedDict
import re
import serial #pip3 install pyserial
import logging
from serial.serialutil import SerialException
from threading import Thread

INIT_VALUES = OrderedDict({
    #Board address, sequence number
    'BAD': None, 'SQN': None,

    # ADC counts from SPEC sensors
    'CMO': None, 'SO2': None, 'NO2': None, 'H2S': None,
    'OZO': None, 'IAQ': None, 'IRR': None,

    #temperatures
    'SHT': None,  'LPT': None, 'HDT': None, 
    'AT0': None, #CO ADC
    'AT1': None, #IAQ/IRR ADC temp
    'AT2': None, #O3/NO2 ADC temp
    'AT3': None, #SO2/H2S ADC temp
    'LTM': None, #CO LMP Temp

    #humidity
    'SHH': None, 'HDH': None,

    #pressure 
    'LPP': None,
     
    #Si1145 sensor (light)
    'SIR': None, 'SUV': None, 'SVL': None, 
})

class PBay(Thread):
    def __init__(self, serial_address, log_filename):
        super(PBay, self).__init__()
        self.measurements = INIT_VALUES
        self._s = serial.Serial(port=serial_address, baudrate=115200, timeout=5) 
        self._p = re.compile('-?[A-Z][A-Z|0-9][A-Z|0-9]{1}=-?[0-9|A-Z]+') #BUG: doesn't handle negative SO2

        # configure logger
        self._log = logging.getLogger('pbay_driver')
        self._log.setLevel(logging.INFO)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(log_filename)
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        self._log.addHandler(fh)
        self._log.addHandler(ch)

    
    def run(self):
        while self._is_running:
            try:
                l = str(self._s.readline())
                self._log.debug("Recived a line: " + l)
                self.parse_and_update_state(l)
                self._log.info("Updated values")
            except SerialException as e:
                self._log.critical("Device disconnected with Exception: {}".format(e))
                self._is_running = False

            #Wrap it in try except once you know how to handle these
            #try:
            #except SerialException as e: #TODO: add error handling
            #    self._log.error(e) 

    def parse_and_update_state(self, data):
        keyvalue_pairs = self._p.findall(data)
        for kv in keyvalue_pairs:
            key = kv[0:3]
            if key in INIT_VALUES.keys():
                self.measurements[key] = kv[4:]
            else:
                self._log.warning("Received an erronous key from the device: " + key)
        
    def __enter__(self):
        self._is_running = True
        self.start()
        while None in self.measurements.values():
            #wait for first batch of measurements to come
            missing_values = [k for k, v in self.measurements.items() if v == None]
            self._log.info("waiting for measurements... Still waiting for: {}".format(missing_values)) 
            time.sleep(1)
        self._log.info("Got all the measurements. Starting.") 
        return self

    def __exit__(self, etype, value, traceback):
        self._is_running = False
        self.join() #TODO: is this right?
        self._s.close()

    def stop(self):
        self._is_running = False


