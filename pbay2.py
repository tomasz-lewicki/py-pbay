import re
import time
import serial #pip3 install pyserial
from threading import Thread

INIT_VALUES = {
    'IRR': None, 'LTM': None, 'HDT': None, 'LPP': None, 'AT0': None,
    'CMO': None, 'SHT': None, 'OZO': None, 'SHH': None, 'BAD': None, 
    'AT2': None, 'SQN': None, 'SO2': None, 'HDH': None, 'NO2': None, 
    'AT3': None, 'AT1': None, 'IAQ': None, 'SIR': None, 'H2S': None,
    'SUV': None, 'SVL': None, 'LPT': None
}

class PBay(Thread):
    def __init__(self, serial_address):
        super(PBay, self).__init__()
        self.measurements = INIT_VALUES
        self._s = serial.Serial(port=serial_address, baudrate=115200, timeout=5) 
        self._p = re.compile('-?[A-Z][A-Z|0-9][A-Z|0-9]{1}=[0-9|A-Z]+')
    
    def run(self):
        while self._is_running:
            l = str(self._s.readline())
            print(l)
            self.parse_line(l)

    def parse_line(self, data):
        keyvalue = self._p.findall(data)
        for kv in keyvalue:
            print(kv)
            self.measurements[kv[0:3]] = kv[4:]
        
    def __enter__(self):
        self._is_running = True
        self.start()
        while None in self.measurements.values():
            #wait for first batch of measurements to come
            time.sleep(1)
            print("waiting for measurements...")
            print(self.measurements)
        return self

    def __exit__(self, etype, value, traceback):
        print(etype,value,traceback)
        self._s.close()
        self._is_running = False

    def stop(self):
        self._is_running = False


if __name__ == '__main__':

    filename = 'dummy'+ str(round(time.time())) +'.csv'
    
    with open(filename, 'w') as logfile:
        logfile.write('timestamp,CMO,H2S,IAQ,IRR,OZO,SO2,NO2\n')

    with PBay('/dev/ttyUSB0') as sensor, open(filename, 'w') as logfile:
        print(sensor.measurements['CMO'])
        logfile.write(
            str(round(time.time()))+','
            + sensor.measurements['CMO']+','
            + sensor.measurements['H2S']+','
            + sensor.measurements['IAQ']+','
            + sensor.measurements['IRR']+','
            + sensor.measurements['OZO']+','
            + sensor.measurements['SO2']+','                  
            + sensor.measurements['NO2']+','
            + '\n'
            )
        
        time.sleep(5)
        