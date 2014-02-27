import codecs
import json
import argparse
import re
import sys
import pysolr
import nltk
from collections import defaultdict

BEFORE_STR = r"(\s?"
AFTER_STR = r"[\s\.\!\?\'\`$])"


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
        self.gold_matches = defaultdict(set)

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

    @property
    def all_documents(self):
        solr_response = self.connection.search("*:*", rows=100)
        all_docs = []
        for response in solr_response:
            title = response["label"]
            body = response["content"]

            all_docs.append(YiddishDocument(response["its_field_doc_id"],
                                            title, body))

        return all_docs

    def get_articles_gold(self, reg_ex_list):
        all_matches = []
        for regex in reg_ex_list:
            match_single_regex = set()
            re_comp = re.compile(BEFORE_STR+regex+AFTER_STR)
            for doc in self.all_documents:
                if re_comp.search(doc.title):
                    match_single_regex.add(doc.doc_id)
                    self.gold_matches[regex].add(re_comp.findall(doc.title)[0])
                if re_comp.search(doc.body):
                    match_single_regex.add(doc.doc_id)
                    self.gold_matches[regex].add(re_comp.findall(doc.body)[0])

            all_matches.append(match_single_regex)
        return all_matches


def read_queries(file_path):
    all_queries = []
    with codecs.open(file_path, "r", "UTF-8") as f_in:
        i = 0
        for line in f_in:
            query_and_regex = line.rstrip().split("\t")
            all_queries.append(query_and_regex)
            i += 1
    return all_queries


def metrics(gold, test, query_strings, verbose=False):
    all_scores = []
    for i, documents_set in enumerate(gold):
        numerator = float(len(documents_set.intersection(test[i])))
        try:
            precision = numerator / len(test[i])
        except ZeroDivisionError:
            precision = 0
        try:
            recall = numerator / len(documents_set)
        except ZeroDivisionError:
            recall = 0
        try:
            f1 = (2*precision*recall)/(precision+recall)
        except ZeroDivisionError:
            f1 = 0
        all_scores.append((precision, recall, f1))
        print query_strings[i], precision, recall, f1

    all_precision,all_recall,all_f1 = zip(*all_scores)
    print "total", sum(all_precision)/len(all_precision),
    print sum(all_recall)/len(all_recall), sum(all_f1)/len(all_f1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("solr_address", help="Solr http address")
    parser.add_argument("-a", "--add", help="path to a json file containing documents")
    parser.add_argument("-q", "--query", help="file containing a list of queries")
    parser.add_argument("-r", "--results", help="show the results of your queries", action="store_true")
    parser.add_argument("-m", "--metrics", help="displays precision, recall and F-measure", action="store_true")
    parser.add_argument("-v", "--verbose", help="display metrics per query", action="store_true")
    parser.add_argument("-s", "--strings", help="shows the strings matched by the regular expressions", action="store_true")

    args = parser.parse_args()
    rms = RednMitSolr(args.solr_address)

    if args.add:
        print "adding documents is deprecated indefinitely"
        #         docs = construct_documents(args.add)
        #         rms.batch_add(docs)
        #         print "Added and committed all documents"
        sys.exit()
    elif args.query:
        title_dictionary = dict((d.doc_id, d.title) for d in rms.all_documents)
        solr_queries, regex_queries = zip(*read_queries(args.query))
        results = rms.batch_query(solr_queries)
        gold_responses = rms.get_articles_gold(regex_queries)
        if args.results:
            for i, q in enumerate(solr_queries):
                print u"Solr Query: {}".format(q)
                for r in results[i]:
                    print u"\tID: {0}\t\tTitle: {1}".format(r, title_dictionary[r])
                print u"\nQueries matched by regex: {}".format(regex_queries[i])
                for g in gold_responses[i]:
                    print u"\tID: {0}\t Title: {1}".format(g, title_dictionary[g])
                print "\n\n"
        elif args.metrics:
            metrics(gold_responses, results, solr_queries)
        elif args.strings:
            for k,v in rms.gold_matches.iteritems():
                print k
                for f in v: print "\t",f
                    