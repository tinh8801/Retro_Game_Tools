'''
Dragon Quest V DS MPT File Structure

32 bytes header gồm:
    4 bytes đầu là MPT0
    4 bytes kế là file size
    4 bytes kế là ID câu thoại đầu
    4 bytes kế là ID câu thoại cuối
    4 bytes kế là tổng số câu thoại trong file
    4 bytes kế là kích thước header (32 bytes)
    4 bytes kế là kích thước của pointer table
    4 bytes cuối kích thước của toàn bộ thoại

Pointer table
Mỗi pointer gồm 6 bytes:
    2 bytes đầu + ID câu thoại đầu => ID câu thoại
    2 bytes kế là kích thước câu thoại (không tính byte padding)
    2 bytes cuối * 4 + kích thước pointer table + kích thước header = offset câu thoại (offset phải là bội số của 4)
    ** Nếu offset tính ra được không phải bội số của 4 thì thêm một hoặc vài byte padding (0xFE) vào cuối câu thoại trước
'''
import argparse
import time

def get_file_info(filename):
    mptfile = open(filename, "rb")
    header = mptfile.read(32)
    info = list()
    header_code = header[0:4]
    info.append(header_code)
    file_size = int.from_bytes(header[4:8], byteorder='little')
    info.append(file_size)
    first_id = int.from_bytes(header[8:12], byteorder='little')
    info.append(first_id)
    last_id = int.from_bytes(header[12:16], byteorder='little')
    info.append(last_id)
    num_of_text = int.from_bytes(header[16:20], byteorder='little')
    info.append(num_of_text)
    header_length = int.from_bytes(header[20:24], byteorder='little')
    info.append(header_length)
    pointer_table_length = int.from_bytes(header[24:28], byteorder='little')
    info.append(pointer_table_length)
    all_text_length = int.from_bytes(header[28:32], byteorder='little')
    info.append(all_text_length)
    mptfile.close()
    return info

def print_file_info(filename):
    info = get_file_info(filename)
    print(info[0])
    print(F"Header length: {info[5]} bytes")
    print(F"File size: {info[1]} bytes")
    print(F"First ID: {info[2]}")
    print(F"Last ID: {info[3]}")
    print(F"Num of message: {info[4]} lines")
    print(F"Pointer table length: {info[6]} bytes")
    print(F"Message length: {info[7]} bytes")

def extract_text(mpt_file, txt_file):
    start_time = time.perf_counter()
    mptfile = open(mpt_file, "rb")
    txtfile = open(txt_file, "w+", encoding="UTF8", newline="\n")
    mptfile.seek(get_file_info(mpt_file)[5])
    pointer_table = mptfile.read(get_file_info(mpt_file)[6])
    
    print("Extracting...")
    for i in range(len(pointer_table) // 6):
        pointer_block = pointer_table[(6 * i):(6 * i + 6)]
        text_id = int.from_bytes(pointer_block[0:2], byteorder='little') + get_file_info(mpt_file)[2]
        text_length = int.from_bytes(pointer_block[2:4], byteorder='little')
        text_offset = int.from_bytes(pointer_block[4:6], byteorder='little')*4 + get_file_info(mpt_file)[6] + get_file_info(mpt_file)[5]
        mptfile.seek(text_offset)
        text_content = mptfile.read(text_length)
        #print(mess_content.decode(encoding="UTF8").replace("\n", "{BREAK}"))
        txtfile.write(F"\n<{text_offset:X}>")
        txtfile.write(text_content.decode(encoding="UTF8", errors="strict").replace("\r\n","{BREAK}"))
    txtfile.write(".")    
    #print("Done")
    mptfile.close()
    txtfile.close()
    end_time = time.perf_counter()
    print(F"Running time: {(end_time - start_time):.3f} second")


def main():
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print(":: Dragon Quest V DS Tool                                                ::")
    print(":: Version: 0.1                                                          ::")
    print(":: Date: 2025.09.10                                                      ::")
    print(":: Tác giả: Huy Thắng                                                    ::")
    print(":: Sử dụng: dq5extractor in_file [-o out_file]                           ::")
    print(":: Ví dụ:                                                                ::")
    print(":: dq5extractor b0000000.mpt                                             ::")
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")

    parser = argparse.ArgumentParser(description="Dragon Quest V DS text extractor")
    parser.add_argument("infile", type=str, help="Tên tập tin .mpt")
    parser.add_argument("-o", "--outfile", type=str, help="Tên tập tin .txt")
    args = parser.parse_args()
    print_file_info(args.infile)
    out_file = args.infile
    out_file = out_file[0:out_file.index(".mpt")] + ".txt"
    if args.outfile==None:
        extract_text(args.infile, out_file)
    else:
        extract_text(args.infile, args.outfile)
    
    
if __name__=="__main__":
    main()
    #extract_text("b0000000_new.mpt", "test.txt")