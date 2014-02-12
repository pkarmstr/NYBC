import nltk
from xml.etree import ElementTree as et
import json
import codecs
import argparse

def crappy_tokenize(path):
    prefix = "{http://www.mediawiki.org/xml/export-0.8/}"
    all_wiki_pages = et.parse(path)
    root = all_wiki_pages.getroot()
    structured_data = {}
    raw_data = {}
    id_ = 0
    for page in root.findall(prefix+"page"):
        title = page.findall(prefix+"title")[0].text
        body = page.findall(prefix+"revision/"+prefix+"text")[0].text
        if title and body:
            tokenized_title = nltk.word_tokenize(title)
            tokenized_body = nltk.word_tokenize(body)
            structured_data[id_] = (tokenized_title, tokenized_body)
            raw_data[id_] = (title, body)
            print u"{0:d} - {1:s}".format(id_, title)
            id_ += 1

    return structured_data, raw_data

def sort_and_scrub(all_articles, max_articles=50):
    sorted_articles = sorted(all_articles.iteritems(), key=lambda d: len(d[1][1]),
                             reverse=True)
    
    good_articles = {}
    num_good = 0
    for id_, (title,body) in sorted_articles:
        if num_good == max_articles:
            break
        print body
        is_good = raw_input("Is this good data? (y/n): ")
        if is_good.startswith("y"):
            good_articles[id_] = (title,body)
            num_good += 1
            print "saving {:s}".format(title)
    
    return good_articles

def save_useful_by_id(file_path, data):
    with codecs.open(file_path, "w", "UTF-8") as yjson:
        yjson.write(json.dumps(data, ensure_ascii=False))
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="file which will be read in")
    parser.add_argument("output_file", help="where to put raw text (in json)")
    parser.add_argument("-a", "--all", help="write all articles to disk (in json)",
                        action="store_true")
    parser.add_argument("-n", "--n_docs", help="number of documents you want to save")
    parser.add_argument("-t", "--tokenize", help="tokenize output location")
    
    args = parser.parse_args()
    
    tokenized,raw = crappy_tokenize(args.input_file)
    print "Done reading in and tokenizing"
    if args.all:
        scrubbed = sort_and_scrub(raw, -1)
    elif args.n_docs:
        scrubbed = sort_and_scrub(raw, args.n_docs)
    else:
        scrubbed = sort_and_scrub(raw)
        
    print "saving files...",
    save_useful_by_id(args.output_file, scrubbed)
    
    if args.tokenize:
        better_tokenized = {}
        for k,_ in scrubbed.iteritems():
            better_tokenized[k] = tokenized[k]
        save_useful_by_id(args.tokenize, better_tokenized)
        
    print "[DONE]"

if __name__ == "__main__":
    main()
