import sys
import time
from pbay import PBay, INIT_VALUES

if __name__ == '__main__':
    #Usage example: python3 pbay.py /dev/ttyUSB1
    csvfilename = 'readings2.csv'
    csvheader = 
    devname = sys.argv[-1]

    #write header
    with open(csvfilename, 'a+') as csvfile:
        for k in INIT_VALUES.keys():
            csvfile.write(k+',')
        csvfile.write('\n')
    
    #open sensor and write the values
    with PBay(devname, 'log.txt') as sensor:
        while(sensor._is_running):
            with open(csvfilename, 'a') as csvfile:
                print(sensor.measurements)
                csvfile.write(str(round(time.time())) + ',')
                for val in sensor.measurements.values():
                    csvfile.write(val + ',')
                
                csvfile.write('\n')
            
            time.sleep(5)
            