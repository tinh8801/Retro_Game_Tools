import argparse

def cuemaker(binpath: str):
    cuename = binpath.split(".bin")[0] + ".cue"
    binname = binpath.split("\\")[-1]
    print(f"Creating...")
    print(cuename)
    try:
        cuefile = open(cuename, "w", encoding="UTF8")
    except:
        print("Error")
        quit()
    cuefile.write(f"FILE \"{binname}\" BINARY")
    cuefile.write("\n")
    cuefile.write("  TRACK 01 MODE2/2352")
    cuefile.write("\n")
    cuefile.write("    INDEX 01 00:00:00")
    cuefile.write("\n")
    print("Done")
    print(f"File {cuename} created")
    cuefile.close()
     
def main():
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print(":: CUE FILE MAKER                                                        ::")
    print(":: Version: 0.1                                                          ::")
    print(":: Date: 2025.04.01                                                      ::")
    print(":: Tác giả: Huy Thắng                                                    ::")
    print(":: Sử dụng: cuemaker BINFILE                                             ::")
    print(":: Ví dụ:                                                                ::")
    print(":: cuemaker Yugioh.bin                                                   ::")
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")

    parser = argparse.ArgumentParser(description="Tạo .CUE cho tập tin .BIN")
    parser.add_argument("binfile", type=str, help="Tên tập tin .bin")
    args = parser.parse_args()
    cuemaker(args.binfile)
     
if __name__=="__main__":
    main()
