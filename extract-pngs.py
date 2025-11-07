# extract_pngs.py
# Extract PNGs from a file and put them in a pngs/ directory
import sys
import os

try:
    os.mkdir("extract_pngs")   
except:
    pass

if len(sys.argv) == 1:
  sys.exit("usage: extract-pngs.py filename")
else:
  file_name=sys.argv[1]
  
      
with open(file_name, "rb") as binary_file:
    binary_file.seek(0, 2)  # Seek the end
    num_bytes = binary_file.tell()  # Get the file size (dem so byte cua file)

    count = 0
    for i in range(num_bytes):
        binary_file.seek(i)
        eight_bytes = binary_file.read(8)
        if eight_bytes == b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a":  # PNG signature
            count += 1
            print("Found PNG Signature #%d at 0x%08x" % (count,i))
            
            with open("extract_pngs/%08x.png" % i, "wb") as outfile:
                outfile.write(eight_bytes)

                while True:
                    sizeData = binary_file.read(4) #Doc 4 byte sau Header de biet kich thuoc chunk (thuong la 0xD=13)
                    
                    size = 4+int.from_bytes(sizeData, byteorder='big', signed=False) #so byte du lieu cua chunk (cong them 4 byte CRC = 17 bytes)
                    
                    chunk = binary_file.read(4) #chunk name (vd: IHDR)
                    
                    outfile.write(sizeData)
                    outfile.write(chunk)
                    
                    data = binary_file.read(size) #doc du lieu cua chunk
                    outfile.write(data)
                    
                    if chunk == b'IEND':
                        break

if count==0:
  print('No PNG in this file')
  