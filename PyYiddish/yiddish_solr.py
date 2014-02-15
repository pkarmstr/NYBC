import codecs
import json
import argparse
import re
import sys
import pysolr

class YiddishDocument:
    def __init__(self, doc_id, title, body_raw, body_tokenized=""):
        self.doc_id = doc_id
        self.title = title
        self.body = body_raw
        self.body_tokenized = body_tokenized

class RednMitSolr:
    
    def __init__(self, address):
        self.address = address
        self.connection = pysolr.Solr(address)
        
    def batch_add(self, docs):
        """do not use - needs to be tested"""
        for doc in docs:
            self.connection.add(doc)
        self.connection.commit()
        
    def batch_query(self, queries_list):
        all_responses = []
        for q in queries_list:
            response_ids = []
            resp = self.connection.search(q, rows=100)
            for r in resp:
                response_ids.append(r["its_field_doc_id"])
            all_responses.append(response_ids)
        return all_responses
            
def construct_documents(file_path):
    all_docs = []
    with codecs.open(file_path, "r", "UTF-8") as f_in:
        all_docs_dict = json.load(f_in)
        for doc_id, (title, body) in all_docs_dict.iteritems():
            all_docs.append(YiddishDocument(doc_id, title, body))
    
    return all_docs

def read_queries(file_path):
    all_queries = []
    with codecs.open(file_path, "r", "UTF-8") as f_in:
        for line in f_in:
            query_and_regex = line.strip("\n").split("\t")
            all_queries.append(query_and_regex)
            
    return all_queries

def get_articles_gold(reg_ex_list, articles):
    all_matches = []
    for regex in reg_ex_list:
        match_single_regex = set()
        re_comp = re.compile(regex)
        for doc in articles:
            if re_comp.match(doc.title) or re_comp.match(doc.body):
                match_single_regex.add(doc.doc_id)
        all_matches.append(match_single_regex)
    return all_matches

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("solr_address", help="Solr http address")
    parser.add_argument("-a", "--add", help="path to a json file containing documents")
    parser.add_argument("-q", "--query", help="file containing a list of queries")
    parser.add_argument("-m", "--metrics", help="displays precision, recall and F-measure")
    parser.add_argument("-v", "--verbose", help="display metrics per query", action="store_true")
    
    args = parser.parse_args()
    rms = RednMitSolr(args.solr_address)
    if args.add:
        print "adding documents is deprecated indefinitely"
#         docs = construct_documents(args.add)
#         rms.batch_add(docs)
#         print "Added and committed all documents"
        sys.exit()
    elif args.query:
        all_qs = read_queries(args.query)
        rms.batch_query(all_qs)
            
