import argparse

def scriptdump(romname):
    try:
        romfile = open(romname, "rb")
        scriptfile = open("dq3_script.txt", "w", encoding="UTF-8")
    except:
        print("Error")
        quit()
    
    table = {0x01:"A", 0x02:"B", 0x03:"C", 0x04:"D", 0x05:"E", 0x06:"F", 0x07:"G", 0x08:"H", 0x09:"I", 0x0A:"J", 0x0B:"K", 0x0C:"L",
             0x0D:"M", 0x0E:"N", 0x0F:"O", 0x10:"P", 0x11:"Q", 0x12:"R", 0x13:"S", 0x14:"T", 0x15:"U", 0x16:"V", 0x17:"W", 0x18:"X",
             0x19:"Y", 0x1A:"Z", 0x1B:"a", 0x1C:"b", 0x1D:"c", 0x1E:"d", 0x1F:"e", 0x20:"f", 0x21:"g", 0x22:"h", 0x23:"i", 0x24:"j",
             0x25:"k", 0x26:"l", 0x27:"m", 0x28:"n", 0x29:"o", 0x2A:"p", 0x2B:"q", 0x2C:"r", 0x2D:"s", 0x2E:"t", 0x2F:"u", 0x30:"v",
             0x31:"w", 0x32:"x", 0x33:"y", 0x34:"z", 0x35:"0", 0x36:"1", 0x37:"2", 0x38:"3", 0x39:"4", 0x3A:"5", 0x3B:"6", 0x3C:"7",
             0x3D:"8", 0x3E:"9", 0x3F:" ", 0x41:"!", 0x42:"\"", 0x43:"#", 0x44:"$", 0x45:"%", 0x46:"&", 0x47:"'", 0x48:"(", 0x49:")",
             0x4A:"*", 0x4B:"+", 0x4C:",", 0x4D:"-", 0x4E:".", 0x4F:"/", 0x50:":", 0x51:";", 0x52:"<", 0x53:"=", 0x54:">", 0x55:"?"}
    
    pointer_start = 0x15331
    pointer_end = 0x1591E
    pointer_size = pointer_end - pointer_start
    
    print("Extracting...")
    print(f"Pointer Start Address: [{pointer_start:X}]")
    print(f"Pointer End Address: [{pointer_end:X}]")
    print(f"Pointer Size: [{pointer_size}] bytes")
    
    pointer_list = list()
    romfile.seek(pointer_start)
    
    for i in range(pointer_size//3 + 1):
        val = romfile.read(3)
        pointer_list.append(int.from_bytes(val, byteorder="little"))
    
    scriptfile.write("#VAR(table, TABLE)")
    scriptfile.write("\n")
    scriptfile.write("#ADDTBL(\"dq3.tbl\", table)")
    scriptfile.write("\n")
    scriptfile.write("#ACTIVETBL(table)")
    scriptfile.write("\n")
    scriptfile.write("#VAR(pointer, CUSTOMPOINTER)")
    scriptfile.write("\n")
    scriptfile.write("#CREATEPTR(pointer, \"LINEAR\", $0, 24)")
    scriptfile.write("\n")
    scriptfile.write("#VAR(pointertable, POINTERTABLE))")
    scriptfile.write("\n")
    scriptfile.write("#PTRTBL(pointertable, $15331, 3, pointer)")
    scriptfile.write("\n")
    scriptfile.write("#JMP($500000)")
    scriptfile.write("\n")
    scriptfile.write("\n")
    scriptfile.write("//===================================================")
    scriptfile.write("\n")
    scriptfile.write("\n")
    
    for i in range(1, len(pointer_list) + 1):
        text = ""
        current_pointer = pointer_list[i - 1]
        print(f"Reading Address: [{current_pointer:X}]")
        
        if i < 506:
            next_pointer = pointer_list[i]
            text_length = next_pointer - current_pointer
        else:
            text_length = 0x8A
            
        print(f"Script Length: [{text_length}] bytes")
        romfile.seek(current_pointer)
        
        for j in range(text_length):
            val = int.from_bytes(romfile.read(1))
            if val in table:
                text += table[val]
            else:
                tmp = "<${0:X}>"
                tmp = tmp.format(val)
                if tmp == "<$AD>":
                    tmp = "<BREAK>\n"
                if tmp == "<$AF>":
                    tmp = "<WAIT>"
                text += tmp
                
        scriptfile.write(f"#WRITE(pointertable)")
        scriptfile.write("\n")
        scriptfile.write(text)
        scriptfile.write("~")
        scriptfile.write("\n")
        scriptfile.write("\n")
        scriptfile.write("//===================================================")
        scriptfile.write("\n")
        scriptfile.write("\n")
        scriptfile.write("//===================================================")
        scriptfile.write("\n")
        scriptfile.write("\n")
        
    scriptfile.close()
    romfile.close()
    print(f"Extracted {pointer_size//3} blocks to file dq3_script.txt")

def main():
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print(":: Dragon Quest 3 SNES Script Extractor                                  ::")
    print(":: Version: 0.1                                                          ::")
    print(":: Date: 2025.04.01                                                      ::")
    print(":: Tác giả: Huy Thắng                                                    ::")
    print(":: Sử dụng: dq3_script_dump.py ROM_file                                  ::")
    print(":: Ví dụ:                                                                ::")
    print(":: dq3_script_dump.py DragonQuest3.sfc                                   ::")
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")

    parser = argparse.ArgumentParser(description="Dragon Quest 3 Script Extractor")
    parser.add_argument("romname", type=str, help="Tên tập tin rom")
    args = parser.parse_args()
    scriptdump(args.romname)
    
if __name__=="__main__":
    main()
    

