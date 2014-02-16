import codecs
import json
import argparse
import re
import sys
import pysolr
import nltk

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
        """do not use - go through drupal"""
        for doc in docs:
            self.connection.add(doc)
        self.connection.commit()
        
    def batch_query(self, queries_list):
        all_responses = []
        for q in queries_list:
            response_ids = set()
            resp = self.connection.search(q, rows=100)
            for r in resp:
                response_ids.add(r["its_field_doc_id"])
            all_responses.append(response_ids)
        return all_responses
            
    def construct_all_documents(self):
        solr_response = self.connection.search("*:*", rows=100)
        all_docs = []
        for response in solr_response:
            title,body = map(nltk.word_tokenize,
                             map(codecs.decode, 
                                 [response["label"],
                                  response["content"]]
                                 )
                             )
            all_docs.append(YiddishDocument(response["its_field_doc_id"],
                                            title,body))
        return all_docs

def read_queries(file_path):
    all_queries = []
    with codecs.open(file_path, "r", "UTF-8") as f_in:
        i = 0
        for line in f_in:
            query_and_regex = line.strip("\n").split("\t")
            all_queries.append(query_and_regex)
            i += 1
    return all_queries

def get_articles_gold(reg_ex_list, articles):
    all_matches = []
    for regex in reg_ex_list:
        match_single_regex = set()
        re_comp = re.compile(regex)
        for doc in articles:
            for token in doc.title:
                if re_comp.match(token):
                    match_single_regex.add(doc.doc_id)
                    break
            for token in doc.body:
                if re_comp.match(token):
                    match_single_regex.add(doc.doc_id)
                    break
        all_matches.append(match_single_regex)
    return all_matches

def metrics(gold, test, verbose=False):
    for i,documents_set in enumerate(gold):
        numerator = float(len(documents_set.intersection(test[i])))
        try:
            precision = numerator/len(test[i])
        except ZeroDivisionError:
            precision = 0
        try:
            recall = numerator/len(documents_set)
        except ZeroDivisionError:
            recall = 0
        print precision, recall

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("solr_address", help="Solr http address")
    parser.add_argument("-a", "--add", help="path to a json file containing documents")
    parser.add_argument("-q", "--query", help="file containing a list of queries")
    parser.add_argument("-r", "--results", help="show the results of your queries", action="store_true")
    parser.add_argument("-m", "--metrics", help="displays precision, recall and F-measure", action="store_true")
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
        all_documents = rms.construct_all_documents()
        title_dictionary = dict((d.doc_id, d.title) for d in all_documents)
        solr_queries,regex_queries = zip(*read_queries(args.query))
        results = rms.batch_query(solr_queries)
        gold_responses = get_articles_gold(regex_queries, all_documents)
        if args.results:
            for i,q in enumerate(solr_queries):
                print "Solr Query: {}".format(q)
                for r in results[i]:
                    print "\tID: {0}\t\tTitle: {1}".format(r, title_dictionary[r])
                print "\nQueries matched by regex: {}".format(regex_queries[i])
                for g in gold_responses[i]:
                    print "\tID: {0}\t Title: {1}".format(g, title_dictionary[g])
                print "\n\n"
        elif args.metrics:
            metrics(gold_responses, results)
                    