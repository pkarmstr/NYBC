import codecs
import re

def open_bad_csv(input_file):
    out = []
    with codecs.open(input_file, "r", "UTF-8") as f_in:
        f_in.readline()
        for line in f_in:
            fields = line.split("|")
            if "=" not in fields[3]:
                out.append((fields[2], fields[3]))
    return out

def align(data):
    """adjusted to have nested charslists"""
    all_words = []
    for titleroman,title in data:
        chars_list= []
        r_tokens = titleroman.split()
        y_tokens = title.split()
        for i,t in enumerate(r_tokens):
            try:
                gut = is_usable(t, y_tokens[i])
            except IndexError:
                break
            if gut:
                cleaner = re.sub(ur"\u0323", "", t)
                chars_list.append(
                                  (list(cleaner.lower().strip()),
                                   list(y_tokens[i].strip())
                                   )
                                  )
        all_words.append(chars_list)
    return all_words
            
def is_usable(roman_token, yiddish_token):
    r_len = len(roman_token)
    y_len = len(yiddish_token)
    if not r_len-3 < y_len < r_len+3:
        return False
    elif re.search("[0-9:\-_\"\.\[\]\(\);\d]", roman_token+yiddish_token) or\
        re.search("[A-Za-z]", yiddish_token):
        return False
    return True

########################################
# functions for making the CRF++ input #
########################################

def write_CRF(training_file, dev_file, test_file, data):
    train = int(len(data)*.7)
    dev = train+int(len(data)*.1)
    write_single_CRF(training_file, data[:train])
    write_single_CRF(dev_file, data[train:dev])
    write_single_CRF(test_file, data[dev:])
    
def write_single_CRF(file_path, data):
    with codecs.open(file_path, "w", "UTF-8") as f_out:
        out_rows = []
        for roman,yiddish in data:
            out_rows.extend(get_CRF_row(roman, yiddish))
        f_out.write("\n".join(out_rows))

def get_CRF_row(roman_token, yiddish_token):
    out_rows = []
    for i,ch in enumerate(roman_token):
        try:
            line = "{}\t{}".format(ch, yiddish_token[i])
        except IndexError:
            line = "{}\tNULL".format(ch)
        out_rows.append(line)
        
    if len(roman_token) < len(yiddish_token):
        for i in range(len(roman_token), len(yiddish_token)):
            line = "NULL\t{}".format(yiddish_token[i])
            out_rows.append(line)
    out_rows.append("")
    return out_rows

#############################################
# functions for making the fast_align input #
#############################################

def write_fast_align(file_path, data):
    with codecs.open(file_path, "w", "UTF-8") as f_out:
        out_rows = []
        for roman_token, yiddish_token in data:
            out_rows.append(" ".join(roman_token) +\
                            " ||| " + " ".join(yiddish_token))
        f_out.write("\n".join(out_rows))


##############################################
# functions for making the Gale-Church input #
##############################################

def write_gale_church(yid_path, roman_path, data):
    with open(yid_path, "w") as yid_out, open(roman_path, "w") as rom_out:
        for title in data:
            for roman_token, yiddish_token in title:
                roman_token = map(lambda s: s.encode("utf-8"), roman_token)
                yiddish_token = map(lambda s: s.encode("utf-8"), yiddish_token)
                rom_out.write("{:s}\n".format(" ".join(roman_token)))
                yid_out.write("{:s}\n".format(" ".join(yiddish_token)))
            rom_out.write("#\n")
            yid_out.write("#\n")

if __name__ == "__main__":
    data = open_bad_csv("resources/ybcorgcollection.csv")
    ready = align(data)
    """
    write_CRF("crf_materials/roman2yiddish_CRF_train.gold", 
              "crf_materials/roman2yiddish_CRF_dev.gold", 
              "crf_materials/roman2yiddish_CRF_test.gold", ready)
    write_fast_align("resources/roman2yiddish_fa.txt", ready)
    """
    write_gale_church("resources/hebrew_char_gacha.txt", "resources/roman_chara_gacha.txt", ready)

    