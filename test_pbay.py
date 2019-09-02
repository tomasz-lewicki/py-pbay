# tests for pbay driver

import unittest
from pbay import *

gas_list = [
    Gas(name='CMO', calib_curr=9851, calib_temp=29.20, nanoamps_per_ppm=4.75, t_const=12, temp_source='AT0'),
    Gas(name='H2S', calib_curr=0, calib_temp=30, nanoamps_per_ppm=212, t_const=13, temp_source='AT3'),
    Gas(name='SO2', calib_curr=0, calib_temp=30, nanoamps_per_ppm=25, t_const=14, temp_source='AT3'),
    Gas(name='IAQ', calib_curr=0, calib_temp=30, nanoamps_per_ppm=30, t_const=12, temp_source='AT1'),
    Gas(name='IRR', calib_curr=0, calib_temp=30, nanoamps_per_ppm=50, t_const=17, temp_source='AT1'),
    Gas(name='NO2', calib_curr=0, calib_temp=30, nanoamps_per_ppm=30, t_const=50, temp_source='AT2'),
    Gas(name='OZO', calib_curr=0, calib_temp=30, nanoamps_per_ppm=30, t_const=50, temp_source='AT2'),
]

class test_pbay(unittest.TestCase):
    
    def __init__(self,*args, **kwargs):
        super(test_pbay, self).__init__(*args, **kwargs)
        self.pbay = PBay(None, 'log.txt', gas_list)

    def test_parse(self):
        line = "BAD=5410ECF75686 SQN=60 SHT=3589 SHH=2958 HDT=3541 HDH=3593 LPT=3672 LPP=101122 SUV=5 SVL=268 SIR=256"
        exp_kv_pairs = ['BAD=5410ECF75686', 'SQN=60', 'SHT=3589', 'SHH=2958', 'HDT=3541', 'HDH=3593', 'LPT=3672', 'LPP=101122', 'SUV=5', 'SVL=268', 'SIR=256']
        kv_pairs = self.pbay._parse(line)
        self.assertListEqual(kv_pairs, exp_kv_pairs)

if __name__ == '__main__':
    unittest.main()