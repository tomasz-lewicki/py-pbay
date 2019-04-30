import re
import time
import serial
import serial.threaded

init_values = {
'IRR': None, 
'LTM': None, 
'HDT': None,
'LPP': None,
'AT0': None,
'CMO': None, 
'SHT': None, 
'OZO': None, 
'SHH': None, 
'BAD': None, 
'AT2': None, 
'SQN': None, 
'SO2': None, 
'HDH': None, 
'NO2': None, 
'AT3': None,
'AT1': None,
'IAQ': None,
'SIR': None,
'H2S': None,
'SUV': None,
'SVL': None,
'LPT': None
}

class PBayParser(serial.threaded.LineReader):
    def __init__(self):
        super(PBayParser, self).__init__()
        self.values = init_values
        self.data = []
        self._p = re.compile('-?[A-Z][A-Z|0-9][A-Z|0-9]{1}=[0-9]+')

    def handle_line(self, data):
        keyvalue = self._p.findall(data)
        for kv in keyvalue:
            self.values[kv[0:3]] = kv[5:]
        

if __name__ == '__main__':
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1)

    #TODO: change this so it's only PBayParser
    with serial.threaded.ReaderThread(ser, PBayParser) as reader: 
        while True:
            print('H2S', reader.values['H2S'], 'SO2', reader.values['SO2'], 'NO2', reader.values['NO2'], 'OZO: ' ,reader.values['OZO'])
            time.sleep(5)

