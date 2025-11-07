#!/usr/bin/python

"""Extract JPG data from files"""
"""Designed intially for Android Thumbdata3 files"""
"""but will work on any file that contains JPG data within it"""

import argparse

parser = argparse.ArgumentParser(description='Name of the file to analyze')

parser.add_argument('-f', '--file', dest='FileName', type=str, help='File containing images to process')

args = parser.parse_args()

#print(args.FileName)

f = open(args.FileName, 'rb')
tdata = f.read() #doc toan bo file thanh String
f.close()

ss = b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a' #PNG header signature
se = b'\x60\x82' #PNG end signature

count = 0
start = 0
while True:
    x1 = tdata.find(ss, start) #tim PNG header signature
    if x1 < 0:
        break
    x2 = tdata.find(se, x1) #tim PNG end signature
    png = tdata[x1:x2+1] #trich xuat 1 phan du lieu tu mang tdata bat dau tu x1 ket thuc o x2+1
    count += 1
    fname = 'extracted%03d.png' % (count)
    fw = open(fname, 'wb')
    fw.write(png)
    fw.close()
    start = x2+2
print(f'Extracted {count} file(s)')