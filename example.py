import sys
import time
from pbay import PBay, INIT_VALUES, Gas  # TODO: hide gases implementation

if __name__ == '__main__':
    # Usage example: python3 pbay.py /dev/ttyUSB1
    csvfilename = 'readings2.csv'
    devname = sys.argv[-1]

    # write header
    with open(csvfilename, 'a+') as csvfile:
        csvfile.write('timestamp,')
        for k in INIT_VALUES.keys():
            csvfile.write(k+',')
        csvfile.write('\n')

    gas_list = [
        Gas(name='CMO', calib_curr=9851, calib_temp=29.20, nanoamps_per_ppm=4.75, t_const=12, temp_source='AT0'),
        Gas(name='H2S', calib_curr=0, calib_temp=30, nanoamps_per_ppm=212, t_const=13, temp_source='AT3'),
        Gas(name='SO2', calib_curr=0, calib_temp=30, nanoamps_per_ppm=25, t_const=14, temp_source='AT3'),
        Gas(name='IAQ', calib_curr=0, calib_temp=30, nanoamps_per_ppm=30, t_const=12, temp_source='AT1'),
        Gas(name='IRR', calib_curr=0, calib_temp=30, nanoamps_per_ppm=50, t_const=17, temp_source='AT1'),
        Gas(name='NO2', calib_curr=0, calib_temp=30, nanoamps_per_ppm=30, t_const=50, temp_source='AT2'),
        Gas(name='OZO', calib_curr=0, calib_temp=30, nanoamps_per_ppm=30, t_const=50, temp_source='AT2'),
        ]

    # open sensor and write the values
    with PBay(serial_address=devname, log_filename='log.txt', gas_list=gas_list) as sensor:
        while(sensor._is_running):
            with open(csvfilename, 'a') as csvfile:
                print(sensor.CMO)
                print(sensor.SO2)
                print(sensor.OZO)
                # csvfile.write(str(round(time.time())) + ',')
                # for val in sensor.measurements.values():
                #     csvfile.write(val + ',')
                # csvfile.write('\n')

            time.sleep(5)
