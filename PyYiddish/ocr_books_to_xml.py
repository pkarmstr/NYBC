import sys
import os
from os.path import join
import xml.etree.cElementTree as ET
import codecs
from collections import namedtuple

__author__ = 'keelan'

if len(sys.argv) != 3:
    sys.exit("usage: ocr_books_to_xml.py [docs_basedir] [xml_output]")

basedir = sys.argv[1]

all_ybc_ids = {}

for f in os.listdir(basedir):
    ybc_id = f[4:-4]
    with codecs.open(join(basedir, f), "r", "utf-8") as f_in:
        book = f_in.read()
        all_ybc_ids[ybc_id] = book

YBCBookInfo = namedtuple("YBCBookInfo", ["YBC_id", "title", "title_roman", "author",
                                         "publisher", "year", "location", "book"])

all_books_meta_data = []
i = 0
with codecs.open("resources/ybcorgcollection.csv", "r", "utf-8") as f_in:
    f_in.readline()
    for line in f_in:
        line = line.split("|")
        if line[0] in all_ybc_ids:
            print line[0]
            ybi = YBCBookInfo(line[0], line[3], line[2], line[1], line[5],
                              line[6], line[4], all_ybc_ids[line[0]])
            all_books_meta_data.append(ybi)

print "found {:d} docs".format(i)
root = ET.Element("root")
sub_doc = ET.SubElement(root, "all_docs")

for ybi in all_books_meta_data:
    subsubdoc = ET.SubElement(sub_doc, "document")
    doc_id_xml = ET.SubElement(subsubdoc, "doc_id")
    doc_id_xml.text = ybi.YBC_id
    title_xml = ET.SubElement(subsubdoc, "title")
    title_xml.text = ybi.title
    body_xml = ET.SubElement(subsubdoc, "body")
    body_xml.text = ybi.book
    tr_xml = ET.SubElement(subsubdoc, "title_roman")
    tr_xml.text = ybi.title_roman
    author_xml = ET.SubElement(subsubdoc, "author")
    author_xml.text = ybi.author
    pub_xml = ET.SubElement(subsubdoc, "publisher")
    pub_xml.text = ybi.publisher
    year_xml = ET.SubElement(subsubdoc, "year")
    year_xml.text = ybi.year
    loc_xml = ET.SubElement(subsubdoc, "location")
    loc_xml.text = ybi.location

tree = ET.ElementTree(root)
tree.write(sys.argv[2], encoding="UTF-8")