# coding=utf-8
__author__ = 'keelan'

import sys
import codecs
import re
import difflib

bad = set(map(lambda x: codecs.decode(x, "utf-8"), map(lambda x: re.sub(r"\s", "", x), ["   דניאל דעראָנהא",
                                                                                        "   דזשאָרדזש עליאֶט",
                                                                                        "דניאל דעראָנדא",
                                                                                        "דניאל דעראָנדא",
                                                                                        "דזשאָרדזש עליאָט",
                                                                                        "דזשאָרדזש על-אָט",
                                                                                        "דני אל דעדאָנדאַ",
                                                                                        "דזשאָרדזש ע?יאָט",
                                                                                        "דניאל דעראָנדאַ",
                                                                                        "דני אל דעראָגדאַ",
                                                                                        "דניאל דעראָנרא",
                                                                                        "דזשאָרדזשׁ עליאֶט",
                                                                                        "געטהע'ס ביאָגראַפיע.",
                                                                                        " ו ו ע ר ט ה ע ר ' ס ל י י ד ע ן .",
                                                                                        "ג ע ט ה ע",
                                                                                        "נ ע ט ה ע",
                                                                                        "ד ע ר",
                                                                                        "פּ ר אָ צ ע ס",
                                                                                        "פֿראַנץ",
                                                                                        " קאַפֿקא",
                                                                                        "ע. ע. פּאָ",
                                                                                        " שריפטען",
                                                                                        "ע. ע. -א",
                                                                                        "דער גערטנער",
                                                                                        "אַ נ נ אַ ק אַ ר ע נ י נ אַ",
                                                                                        "ל. נ. ס אָ ל ס ס אָ י"])))

if len(sys.argv) != 3:
    sys.exit("usage: process.py input.txt output.txt")

all_lines = []

with codecs.open(sys.argv[1], "r", "utf-8") as f_in:
    for line in f_in:
        line = line.rstrip().strip()
        if line.startswith("Page") or \
                difflib.get_close_matches(re.sub(r"\s", "", line), bad) or \
                line.startswith("____") or \
                re.match(ur"\.?(\u2014)?\s?\d+\s?(\u2014)?\.?", line) or \
                        0 < len(line) < 3:
            continue
        all_lines.append(line)

better = []

i = 0
while i < len(all_lines):
    try:
        if all_lines[i] == u"" and all_lines[i+1] == u"":
            while all_lines[i] == u"" and i < len(all_lines):
                i += 1
        better.append(all_lines[i])
    except IndexError:
        pass
    i += 1


with codecs.open(sys.argv[2], "w", "utf-8") as f_out:
    f_out.write("\n".join(better))

print "finished, wrote to", sys.argv[2]