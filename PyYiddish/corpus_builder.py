import nltk
from xml.etree import ElementTree as et
import json
import codecs

def crappy_tokenize(path):
    prefix = "{http://www.mediawiki.org/xml/export-0.8/}"
    all_wiki_pages = et.parse(path)
    root = all_wiki_pages.getroot()
    structured_data = []
    raw_data = []
    id_ = 0
    for page in root.findall(prefix+"page"):
        title = page.findall(prefix+"title")[0].text
        body = page.findall(prefix+"revision/"+prefix+"text")[0].text
        if title and body:
            tokenized_title = nltk.word_tokenize(title)
            tokenized_body = nltk.word_tokenize(body)
            structured_data.append((id_, tokenized_title, tokenized_body))
            #raw_data.append(u"{0} || {1} || {2}".format(id_, title, body))
            print u"{0:d} - {1:s}".format(id_, title)
            id_ += 1

    print "[DONE]"
    return structured_data, raw_data

if __name__ == "__main__":
    path = "/home/keelan/Desktop/yiwiki-latest-pages-articles.xml"
    tokens,raw = crappy_tokenize(path)
    
    with codecs.open("yiddish_corpus.json", "w", "UTF-8") as yjson:
        yjson.write(json.dumps(tokens, ensure_ascii=False))
    """
    with codecs.open("raw_yiddish_corpus.txt", "w", "UTF-8") as ycorp:
        ycorp.write("\n\n\n\n".join(raw))
	"""
    print "Super Done"
