import sys
import codecs
import json
import xml.etree.cElementTree as ET

if len(sys.argv) != 4:
    sys.exit("Usage: json_to_xml.py [json_file] [xml_file1] [xml_file2]")
    
with codecs.open(sys.argv[1], "r", "UTF-8") as f_in:
    j = json.load(f_in)
    
root = ET.Element("root")
sub_doc = ET.SubElement(root, "all_docs")
json_iterator = j.iteritems()
i=0
for doc_id, (title,body) in json_iterator:
    if i == 20:
        break
    
    i+=1
    subsubdoc = ET.SubElement(sub_doc, "document")
    doc_id_xml = ET.SubElement(subsubdoc, "doc_id")
    doc_id_xml.text = doc_id
    title_xml = ET.SubElement(subsubdoc, "title")
    title_xml.text = title
    body_xml = ET.SubElement(subsubdoc, "body")
    body_xml.text = body
    
tree = ET.ElementTree(root)
tree.write(sys.argv[2], encoding="UTF-8")

root = ET.Element("root")
sub_doc = ET.SubElement(root, "all_docs")

for doc_id, (title,body) in json_iterator:
    subsubdoc = ET.SubElement(sub_doc, "document")
    doc_id_xml = ET.SubElement(subsubdoc, "doc_id")
    doc_id_xml.text = doc_id
    title_xml = ET.SubElement(subsubdoc, "title")
    title_xml.text = title
    body_xml = ET.SubElement(subsubdoc, "body")
    body_xml.text = body
    
tree = ET.ElementTree(root)
tree.write(sys.argv[3], encoding="UTF-8")