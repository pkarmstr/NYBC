import codecs
import json
import argparse
import re
import sunburnt

class YiddishDocument:
    def __init__(self, doc_id, title, body_raw, body_tokenized=""):
        self.doc_id = doc_id
        self.title = title
        self.body = body_raw
        self.body_tokenized = body_tokenized

class RednMitSolr:
    
    def __init__(self, address, schema=None):
        self.address = address
        self.schema = schema
        if schema:
            self.connection = sunburnt.SolrInterface(address, schema)
        else:
            self.connection = sunburnt.SolrInterface(address)
        
    def batch_add(self, docs):
        for doc in docs:
            self.connection.add(doc)
        self.connection.commit()
        
    def batch_query(self, queries_list):
        for q in queries_list:
            resp = self.connection.query(q).execute()
            print resp.result
            
def construct_documents(file_path):
    all_docs = []
    with codecs.open(file_path, "r", "UTF-8") as f_in:
        all_docs_dict = json.load(f_in)
        for doc_id, (title, body) in all_docs_dict.iteritems():
            all_docs.append(YiddishDocument(doc_id, title, body))
    
    return all_docs

def read_queries(file_path):
    all_queries = []
    with codecs.open(args.query, "r", "UTF-8") as f_in:
        for line in f_in:
            query_and_regex = line.strip("\n").split("\t")
            all_queries.append(query_and_regex)
            
    return all_queries

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("solr_address", help="Solr http address")
    parser.add_argument("-s", "--schema", help="schema file used by running instance of Solr")
    parser.add_argument("-a", "--add", help="path to a json file containing documents")
    parser.add_argument("-q", "--query", help="file containing a list of queries")
    parser.add_argument("-m", "--metrics", help="displays precision, recall and F-measure")
    parser.add_argument("-v", "--verbose", help="display metrics per query", action="store_true")
    
    args = parser.parse_args()
    rms = RednMitSolr(args.solr_address)
    if args.add:
        docs = construct_documents(args.add)
        rms.batch_add(docs)
        print "Added and committed all documents"
    elif args.query:
        all_qs = read_queries(args.query)
        rms.batch_query(all_qs)
            
