import os
import sys
import errno

#Usage in cmd: python hexread.py Test.bin
#              python hexread.py

if len(sys.argv) !=1:
    print("Selecting file..."+sys.argv[1])
else:
    filename=input("Enter Filename or press ENTER to skip: ")
    if filename == '':
        sys.exit("No Args or filename, exiting")
    else:
        sys.argv.append(filename)
        print("Selecting file..."+sys.argv[1])

with open(sys.argv[1], "rb") as binary_file:
    print("Opening file:"+sys.argv[1])
    binary_file.seek(0, 2)  # Seek the end
    num_bytes = binary_file.tell()  # Get the file size
    print('File size:'+str(num_bytes)+'B')
    count = 0
    print('Finding PNG signatures')
    for i in range(num_bytes):
        binary_file.seek(i)
        eight_bytes = binary_file.read(8)
        if eight_bytes == b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a":  # PNG signature
            count += 1
            print("Found PNG Signature #" + str(count) + " at " + str(i))
            try:
                os.mkdir('png_files')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            with open("png_files/" + str(i) + ".png", "wb") as outfile:
                outfile.write(eight_bytes)
            # Read all chunk in PNG block and write to file
                while True:
                    chunk_size = binary_file.read(4) #read 4 bytes to know a chunk size
                    chunk_bytes_num = int.from_bytes(chunk_size, byteorder='big', signed=False) + 4 #a chunk's num of bytes = chunk_size + 4 bytes CRC
                    outfile.write(chunk_size)
                    chunk_name = binary_file.read(4) #read 4 bytes to know a chunk name
                    outfile.write(chunk_name)
                    chunk_data = binary_file.read(chunk_bytes_num) #read all chunk data bytes
                    outfile.write(chunk_data)
                    if chunk_name == b"IEND":
                        break
            
            
if count==0:
    print('No PNG signatures found!')