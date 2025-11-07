#!/usr/bin/env python

# please ensure python means python3 on your system
# the file can be any binary file that contains a JPG image
# note that it's hungry and doesn't chunk the read so careful with large files

# usage: extract-image file_name

import sys
try:
  file_name = sys.argv[1]
except:
    print('usage: extract-image.py file_name')
    sys.exit()

def extract_jpg_image():
  jpg_byte_start = b'\xff\xd8'
  jpg_byte_end = b'\xff\xd9'
  jpg_image = bytearray()
  jpgs_list=[]
  pos=0
  start=0
  with open(file_name, 'rb') as f:
    req_data = f.read()
  while start != -1:
    start = req_data.find(jpg_byte_start, pos)

    #if start == -1:
      #print('Could not find JPG start of image marker!')
      #return

    end = req_data.find(jpg_byte_end, start) + len(jpg_byte_end)
    jpg_image = req_data[start:end]
    jpgs_list.append(jpg_image)
    pos=end
    print(f'Size: {end - start} bytes')
    
  for i in range(len(jpgs_list)-1):
    with open(f'{file_name}-extracted-img{i}.jpg', 'wb') as f:
      f.write(jpg_image)
    
def extract_png_image():
  png_byte_start = b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'
  png_byte_end = b'\x60\x82'
  png_image = bytearray()
  pngs_list=[]
  pos=0
  start=0
  with open(file_name, 'rb') as f:
    req_data = f.read()
    
  while start != -1:
    start = req_data.find(png_byte_start, pos)

    #if start == -1:
      #print('Could not find PNG start of image marker!')
      #return

    end = req_data.find(png_byte_end, start) + len(png_byte_end)
    png_image = req_data[start:end]
    pngs_list.append(png_image)
    pos=end
    print(f'Size: {end - start} bytes')

  for i in range(len(pngs_list)-1):    
    with open(f'{file_name}-extracted-img{i}.png', 'wb') as f:
      f.write(pngs_list[i])

if __name__ == "__main__":
  extract_png_image()
