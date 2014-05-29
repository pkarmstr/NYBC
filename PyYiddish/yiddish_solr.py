import codecs
import json
import argparse
import re
import sys
import pysolr
import nltk
from collections import defaultdict

__author__ = "Keelan Armstrong <pkarmstr at gmail dot com>"

BEFORE_STR = r"([\s\)\]]?"
AFTER_STR = r"[\s\.\!\?\'\`\]\)$])"

class YiddishDocument:
    def __init__(self, doc_id, title, body_raw, body_tokenized=""):
        self.doc_id = doc_id
        self.title = title
        self.body = body_raw
        self.body_tokenized = body_tokenized


class RednMitSolr:
    """A class to talk to a Solr installation which contains a number of yiddish documents"""

    def __init__(self, address):
        self.address = address
        self.connection = pysolr.Solr(address)
        self.all_documents = self.get_all_documents()
        self.gold_matches = defaultdict(set)

    def batch_add(self, docs):
        """do not use - go through drupal"""
        for doc in docs:
            self.connection.add(doc)
        self.connection.commit()

    def batch_query(self, queries_list):
        """queries solr, keeps an ordered list of the doc ID's of the responses

        :param queries_list: a list of strings to sent to Solr

        """
        all_responses = []
        for q in queries_list:
            response_ids = set()
            resp = self.connection.search(q, rows=100)
            for r in resp:
                response_ids.add(r["its_field_doc_id"]) #this is fragile...
            all_responses.append(response_ids)
        return all_responses

    def get_all_documents(self):
        """retrieves all documents from the Solr installation for regular
        expression queries

        """
        solr_response = self.connection.search("*:*", rows=100)
        all_docs = []
        for response in solr_response:
            try:
                title = response["label"]
                body = response["content"]
                all_docs.append(YiddishDocument(response["its_field_doc_id"],
                                                title, body))
            except KeyError:
                continue

        return all_docs

    def get_articles_gold(self, reg_ex_list):
        """takes a list of regular expressions, searches each document
        and creates a ``gold standard'' of what a query should return

        """
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
    """reads a tab separated file, in the form of:

    solr-query    regular-expression

    """
    all_queries = []
    with codecs.open(file_path, "r", "UTF-8") as f_in:
        i = 0
        for line in f_in:
            query_and_regex = line.rstrip().split("\t")
            all_queries.append(query_and_regex)
            i += 1
    return all_queries


def metrics(gold, test, query_strings, verbose=False):
    """calculates precision, recall and f-measure, given a gold standard
    and test set, and pretty prints the results with the query. Ordering
    is very important!

    """
    all_numerator = 0
    all_recall_denom = 0
    all_precision_denom = 0
    print u"{:10s} {:7s}  {:7s}  {:7s}".format("query", "precision", "recall", "f1", align="center")
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
        all_numerator += numerator
        all_precision_denom += len(test[i])
        all_recall_denom += len(documents_set)

        print u"{:10s} {:7.2f}  {:7.2f}  {:7.2f}".format(query_strings[i], precision, recall, f1)

    precision = all_numerator/all_precision_denom
    recall = all_numerator/all_recall_denom
    f1 = (2*precision*recall)/(precision+recall)
    print u"{:10s} {:7.2f}  {:7.2f}  {:7.2f}".format("Total", precision, recall, f1)


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
        print "adding documents is disabled indefinitely"
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
                for f in v: print "\t",f[0]