# py-pbay
A python driver for SPEC Sensors PBay board

# Getting started
## 1. Install
```
pip3 install pbay
```
## 2. Run examples

To simply display values:
```bash
python3 example.py /dev/ttyUSB0
``` 

To log values to a csv file:
```bash
python3 example_csv.py /dev/ttyUSB0
```

Your devpath for PBay can be different than ```/dev/ttyUSB0```.
To check it, use ```dmesg``` command after connecting USB and examine the output.

## 3. Calibration
Before use, be sure to override the values in examples with your own calibration values
