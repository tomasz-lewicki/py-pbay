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
            self.values[kv[0:3]] = kv[4:]

if __name__ == '__main__':
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1)

    filename = 'log'+ str(round(time.time())) +'.csv'
    with open(filename, 'w') as file:
        file.write('timestamp,CMO,H2S,IAQ,IRR,OZO,SO2,NO2\n')
    
    #BUG: exits on any exception in reader thread. Should be a daemon that keep trying

    with serial.threaded.ReaderThread(ser, PBayParser) as reader: 
        while True:

            if None not in reader.values.values(): #don't output to csv until all values are populated

                with open(filename, 'a') as file:
                    file.write(
                        str(round(time.time()))+','
                        + reader.values['CMO']+','
                        + reader.values['H2S']+','
                        + reader.values['IAQ']+','
                        + reader.values['IRR']+','
                        + reader.values['OZO']+','
                        + reader.values['SO2']+','                  
                        + reader.values['NO2']+','
                        + '\n'
                        )
            
            time.sleep(5)

