import argparse

def findtextend(romname):
    try:
        romfile=open(romname, "rb+")
    except:
        print("Error")
        quit()
    romfile.seek(0x1591C)
    val = romfile.read(3)
    last_pointer = int.from_bytes(val, byteorder="little")
    print(f"{last_pointer:X}")
    romfile.seek(last_pointer)
    val = romfile.read(0x8A)
    pos = val.find(b'\x01\x2C\x2C\x1B\x28\x21\x1F\x27\x1F\x28\x2E\x3F\x35\x3B\x55\xAC')
    romfile.close()
    return last_pointer + pos

def fixrom(romname):
    try:
        romfile=open(romname, "rb+")
    except:
        print("Error")
        quit()
        
    romfile.seek(0x500000)
    end_pos = findtextend(romname) #0x53E12E
    count = 0
    while romfile.tell() < end_pos:
        val = romfile.read(1)
        if val == bytes([0]):
            count += 1
            romfile.seek(romfile.tell()-1)
            romfile.write(bytes([0xAC]))
    print(f"Fixed {count} bytes")

def main():
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print(":: Dragon Quest 3 SNES Data Fix                                          ::")
    print(":: Version: 0.1                                                          ::")
    print(":: Date: 2025.04.01                                                      ::")
    print(":: Tác giả: Huy Thắng                                                    ::")
    print(":: Sử dụng: fix_rom.py ROM_file                                          ::")
    print(":: Ví dụ:                                                                ::")
    print(":: fix_rom.py DragonQuest3.sfc                                           ::")
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")

    parser = argparse.ArgumentParser(description="Dragon Quest 3 Data Fix")
    parser.add_argument("romname", type=str, help="Tên tập tin rom")
    args = parser.parse_args()
    fixrom(args.romname)


if __name__=="__main__":
    main()