import argparse
import os

def setbit(b: int, pos: int) -> int:
    i = 1
    i = i << pos
    return b ^ i

def getbit(b: int, pos: int) -> int:
    val = b >> pos
    return val & 0x01

def countbit(b: int) -> int:
    count = 0
    for i in range(0, 8):
        if ((b >> i) & 0x01) == 1:
            count += 1
    return count

def getfilesize(filename: str) -> int:
    return os.path.getsize(filename)

def mostfrequent(lst: list):#Xác định byte lặp lại nhiều lần nhất trong block 8 bytes
    #return max(set(l), key=l.count)
    #return sorted(set(l), key=lambda x: l.count(x), reverse=True)[0]
    checked = dict()
    
    for item in lst:
        if item not in checked.keys():
            checked[item] = 1
        else:
            checked[item] += 1
            
    if len(checked) == 8:#Nếu không có byte nào lặp lại
        return -1
    else:
        for item in checked.items():#Xác định byte nào lặp lại nhiều nhất
            if (item[1] > 1):
                return item[0]
                break

def infobyte(lst: list) -> int:#Tính ra byte mô tả khối dữ liệu được nén
    val = 0xFF
    for i in range(0, 8):
        if mostfrequent(lst) == -1:#Nếu không byte nào lặp lại
            val = 0x7F
        else:
            if lst[i] == mostfrequent(lst):
                val = setbit(val, 7-i)
    return val

def decode(infile: str, outfile: str, fontpos: int):#Giải nén font
    try:
        romfile = open(infile, "rb")
        fontfile = open(outfile, "wb")
    except:
        print("Lỗi đọc ghi tập tin")
        quit()
        
    print("Bắt đầu giải nén...")
    romfile.seek(fontpos) #Font ở vị trí 0x100000
    data = list()
    byte_count = 0
    for a in range(0, 0x200):
        infobyte = int.from_bytes(romfile.read(1))
        #print(f"Info byte [{infobyte:X}]")
        for b in range(0, countbit(infobyte) + 1):
            data.append(romfile.read(1))
        #print(data)
        n = 0
        for c in range(7, -1, -1):
            if getbit(infobyte, c) == 0:
                fontfile.write(bytes(data[0]))
            else:
                fontfile.write(bytes(data[1 + n]))
                n += 1
        data=[]
        
    romfile.close()
    fontfile.close()
    print(f"Đã giải nén ra tập tin {outfile}")
    return 0
        
#val = sorted(checked.items(), key = lambda x: x[0])[0]

def encode(infile: str, outfile: str):#Nén font
    try:
        fontfile = open(infile, "rb")
        encodedfont = open(outfile, "wb")
    except:
        print("Lỗi đọc ghi tập tin")
        quit()
    print("Bắt đầu nén...")
    data_block=list()
    font_block=list()
    
    while fontfile.tell() < getfilesize(infile):
        
        for i in range(0, 8):
            data_block.append(int.from_bytes(fontfile.read(1)))#Đọc từng khối 8 bytes
            
        info_byte = infobyte(data_block) #Tính byte mô tả khối dữ liệu sau nén
        font_block.append(info_byte)

        if mostfrequent(data_block) != -1:
            font_block.append(mostfrequent(data_block))
            
        for i in range(0, 8):
            if data_block[i] != mostfrequent(data_block):
                font_block.append(data_block[i])
        data_block = []
        
    for i in font_block:
        encodedfont.write(bytes([i]))
        
    encodedfont.close()
    fontfile.close()
    print(f"Đã nén thành tập tin {outfile}")
    return 0
    
def insert(romname: str, fontname: str):
    try:
        encode(fontname, "tmp.bin")
    except:
        print("Lỗi đọc ghi tập tin")
        quit()
    
    try:
        romfile = open(romname, "rb+")
        fontfile = open("tmp.bin", "rb")
    except:
        print("Lỗi đọc ghi tập tin")
        quit()
        
    print("Bắt đầu ghi vào rom...")
    dat = fontfile.read()
    romfile.seek(0x100000)
    
    if len(dat) <= 0xE5C:
        for i in dat:
            romfile.write(bytes([i]))
        for i in range(0xE5C - len(dat)):
            romfile.write(bytes([0]))
    else:
        print("Font lớn hơn kích thước gốc")
                    
    romfile.close()
    fontfile.close()
    print(f"Đã ghi tập tin {fontname} vào {romname}")
    try:
        os.remove("tmp.bin")
    except:
        print("Lỗi đọc ghi tập tin")
    return 0
        
def main():
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print(":: Aladdin SNES Font Tool                                                ::")
    print(":: Version: 0.1                                                          ::")
    print(":: Date: 2025.04.01                                                      ::")
    print(":: Tác giả: Huy Thắng                                                    ::")
    print(":: Sử dụng: Aladdin_Font_Tool.py [option] ROM_file                       ::")
    print(":: Ví dụ:                                                                ::")
    print(":: Aladdin_Font_Tool.py -x \"Aladdin (USA).sfc\"                           ::")
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")

    parser = argparse.ArgumentParser(description="Aladdin SNES Font Tool")
    parser.add_argument("-x", "--extract", action="store_true", help="Giải nén font")
    parser.add_argument("-i", "--insert", action="store_true", help="Ghi font vào rom")
    parser.add_argument("romname", type=str, help="Tên tập tin rom")
    args = parser.parse_args()
    
    if args.insert:
        insert(args.romname, "aladdin_font.bin")
    elif args.extract:
        decode(args.romname, "aladdin_font.bin", 0x100000)
    else:
        print("Thiếu tham số")
    
if __name__=="__main__":
    main()
        
        
        
        
    
    
    
