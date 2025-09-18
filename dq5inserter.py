#Dragon Quest V DS Script Inserter

import os

def check_line_start(l: str) -> bool:#Kiểm tra câu thoại có bắt đầu bằng <> không
    if l.startswith("<"):
        return True
    else:
        return False
    
def available_offset(offset: int) -> int:#Tìm offset thỏa mãn điều kiện chia hết cho 4
    while(offset %4 != 0):
        offset += 1
    return offset

def get_mpt_size(filename: str) -> int:#Xác định kích thước tập tin mpt
    return os.path.getsize(filename)

def update_pointer_length_val(mpt, pointer_num: int, val: int) -> int:#Cập nhật lại giá trị text length của pointer
    mpt.seek(32 + (6 * pointer_num) + 2)
    mpt.write(val)
    return 0

def update_pointer_offset_val(mpt, pointer_num: int, val: int):#Cập nhật lại giá trị offset của pointer
    mpt.seek(32 + (6 * pointer_num) + 4)
    mpt.write(val)
    return 0

def update_header_filesize(mpt, val):#Cập nhật lại giá trị file size của header
    mpt.seek(4)
    mpt.write(val)
    return 0

def update_header_textlength(mpt, val):#Cập nhật lại giá trị text length của header
    mpt.seek(28)
    mpt.write(val)
    return 0

def get_pointer_table(filename: str):#Lấy toàn bộ pointer table
    f = open(filename, "rb")
    info = get_mpt_info(filename)
    header_length = info[5]
    pointer_table_length = info[6]
    f.seek(header_length)
    pointer_table_list = f.read(pointer_table_length)
    return pointer_table_list

def get_first_offset(filename: str) -> int:#Tìm offset câu thoại đầu tiên
    pointer_table = get_pointer_table(filename)
    info = get_mpt_info(filename)
    first_block = pointer_table[0:6]
    first_offset = int.from_bytes(first_block[4:6], byteorder='little') * 4 + len(pointer_table) + info[5]
    return first_offset
    
def recalculate_pointer(offset, pointer_table_length, header_length):#Tính lại giá trị offset mới
    val = (offset - pointer_table_length - header_length)//4
    return val

def get_mpt_info(filename: str):#Lấy thông tin file mpt
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

'''
def insert_script(script_file, mpt_file, new_mpt_file):
    scriptfile = open(script_file, "r", encoding="UTF8")
    mpt_info = get_mpt_info(mpt_file)
    bytes_to_copy = mpt_info[6] + mpt_info[5]
    mptfile = open(mpt_file, "rb")
    newmptfile = open(new_mpt_file, "wb+")
    data = mptfile.read(bytes_to_copy)
    newmptfile.write(data)
    lines = scriptfile.readlines()
    pointer_table = get_pointer_table(mpt_file)
    current_offset = get_first_offset(mpt_file)
    l = 0
    count = 0

    while l < len(lines):#Duyệt qua tất cả các dòng của file text
        content = ""
        line = ""
        offset = current_offset
        new_pointer_val = recalculate_pointer(offset, len(pointer_table), mpt_info[5])
        end_pos = 0
        av_offset = 0
        
        if check_line_start(lines[l]):
            line = lines[l]
            for m in range(l + 1, len(lines)):
                if check_line_start(lines[m]):
                    break    
                else:
                    line += lines[m]
                    l += 1
            count +=1
        
        else:
            print("Invalid Line Skipped")
            l += 1
            continue 
        #line=line.replace("\n", "")
        line = line.replace("{BREAK}", "\r\n")
        i = line.index(">")
        content = line[i + 1:-1]
        array = content.encode()
        update_pointer_length_val(newmptfile, count-1, len(array).to_bytes(2, "little"))
        update_pointer_offset_val(newmptfile, count-1, new_pointer_val.to_bytes(2, "little"))
        end_pos = offset + len(array)
        av_offset = available_offset(end_pos)
        #if l==len(lines)-1:
        if count == mpt_info[4]:
            av_offset = end_pos
        
        if av_offset != end_pos:
            for a in range(av_offset - end_pos):
                array += b'\xFE'
            newmptfile.seek(offset)
            newmptfile.write(array)
        else:
            newmptfile.seek(offset)
            newmptfile.write(array)

        l += 1
        current_offset = av_offset
        
    newmptfile.flush()
    newfilesize = get_mpt_size(new_mpt_file)
    new_mpt_info = get_mpt_info(new_mpt_file)
    new_all_text_length = newfilesize - len(pointer_table) - new_mpt_info[5]
    newfilesize = newfilesize.to_bytes(2, "little")
    update_header_filesize(newmptfile, newfilesize)
    new_all_text_length = new_all_text_length.to_bytes(2, "little")
    update_header_textlength(newmptfile, new_all_text_length)
    newmptfile.close()
    mptfile.close()
    scriptfile.close()
    print(F"{count} lines inserted")
    print("Done")
'''

def replace_vietnamese_char(l: str) -> str:
    vietnamese_chars = ["ấ", "ầ", "ẩ", "ẫ", "ậ", "ă", "ắ", "ằ", "ẳ", "ẵ", "ặ", "ế", "ề", "ể", "ễ", "ệ", "ố", "ồ", "ổ", "ỗ", "ộ", "ơ", "ớ",
                       "ờ", "ở", "ỡ", "ợ", "ư", "ứ", "ừ", "ử", "ữ", "ự", "ả", "ạ", "ẻ", "ẽ", "ẹ", "ỉ", "ĩ", "ị", "ỏ", "ọ", "ủ", "ũ", "ụ",
                       "ỳ", "ỷ", "Đ", "đ"]
    replace_chars = ["Ё", "А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х",
                     "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я", "ä", "ß", "ç", "ë", "æ", "î", "ï", "œ", "ö", "ñ", "û", "ü", "ø",
                     "Œ", "ÿ", "Ð", "ð"]
    for i in range(len(l)):
        if l[i] in vietnamese_chars:
            n = vietnamese_chars.index(l[i])
            l = l.replace(l[i], replace_chars[n])
    return l
    
def insert_script_overwrite(script_file, new_mpt_file):
    scriptfile = open(script_file, "r", encoding="UTF8")
    mpt_info = get_mpt_info(new_mpt_file)
    newmptfile = open(new_mpt_file, "rb+")
    lines = scriptfile.readlines()
    pointer_table = get_pointer_table(new_mpt_file)
    current_offset = get_first_offset(new_mpt_file)
    l = 0
    count = 0

    while l < len(lines):#Duyệt qua tất cả các dòng của file text
        content = ""
        line = ""
        offset = current_offset
        new_pointer_val = recalculate_pointer(offset, len(pointer_table), mpt_info[5])
        end_pos = 0
        av_offset = 0
        
        if check_line_start(lines[l]):
            line = lines[l]
            for m in range(l + 1, len(lines)):
                if check_line_start(lines[m]):
                    break    
                else:
                    line += lines[m]
                    l += 1
            count +=1
        
        else:
            print("Invalid Line Skipped")
            l += 1
            continue 
        #line=line.replace("\n", "")
        line = line.replace("{BREAK}", "\r\n")
        
        i = line.index(">")
        content = line[i + 1:-1]
        content = replace_vietnamese_char(content)
        array = content.encode()
        update_pointer_length_val(newmptfile, count - 1, len(array).to_bytes(2, "little"))
        update_pointer_offset_val(newmptfile, count - 1, new_pointer_val.to_bytes(2, "little"))
        end_pos = offset + len(array)
        av_offset = available_offset(end_pos)
        #if l==len(lines)-1:
        if count == mpt_info[4]:
            av_offset = end_pos
        
        if av_offset != end_pos:
            for a in range(av_offset - end_pos):
                array += b'\xFE'
            newmptfile.seek(offset)
            newmptfile.write(array)
        else:
            newmptfile.seek(offset)
            newmptfile.write(array)

        l += 1
        current_offset = av_offset
        
    newmptfile.flush()
    newfilesize = get_mpt_size(new_mpt_file)
    new_mpt_info = get_mpt_info(new_mpt_file)
    new_all_text_length = newfilesize - len(pointer_table) - new_mpt_info[5]
    newfilesize = newfilesize.to_bytes(2, "little")
    update_header_filesize(newmptfile, newfilesize)
    new_all_text_length = new_all_text_length.to_bytes(2, "little")
    update_header_textlength(newmptfile, new_all_text_length)
    newmptfile.close()
    scriptfile.close()
    print(F"{count} lines inserted")
    print("Done")  

    
#insert_script("test.txt", "b0000000_orig.mpt", "b0000000.mpt")
insert_script_overwrite("test.txt", "b0000000.mpt")
    