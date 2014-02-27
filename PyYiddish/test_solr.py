#!/usr/bin/python
# -*- coding: UTF-8 -*-

import codecs
import unittest
from yiddish_solr import *

class SolrYiddishTest(unittest.TestCase):
    """a simple test suite to check that my connection with Solr is executing 
    queries correctly and returning results, as well as other functionalities
    within the yiddish_solr file
    
    """
    
    def setUp(self):
        self.rms = RednMitSolr("http://localhost:8983/solr")
        self.yiddish_queries = map(lambda x: codecs.decode(x,"UTF-8"),\
                                   ["לעצט", "ברודער", "קאמוניזם"])
        self.articles = self.rms.all_documents
        self.queries,self.regexes = zip(*read_queries("resources/yid_regex"))
        
    
    def test_simple(self):
        """make sure we can handle a simple single query"""
        resp = self.rms.connection.search(self.yiddish_queries[0], rows=50)
        self.assertGreater(len(resp.docs), 0)
            
    def test_get_all_docs(self):
        """making sure we have access to all of the documents"""
        resp = self.rms.connection.search("*:*", rows=100)
        self.assertEqual(len(resp.docs), 50)
            
    def test_batch_query(self):
        """see if the class function works properly"""
        self.resp = self.rms.batch_query(self.yiddish_queries)
        self.assertEqual(len(self.resp), 3)
        
    def test_regex_matching(self):
        """make sure the regular expression works on a synthetic example"""
        yd = YiddishDocument(36, codecs.decode("מיין ברודער", "UTF-8"), "")
        bruder = self.regexes[0]
        match = self.rms.get_articles_gold([bruder])
        self.assertEqual(36, list(match[0])[0])
        
    def test_regex_all_docs(self):
        """test that the regular expressions are at least matching a single doc"""
        match = self.rms.get_articles_gold(self.regexes)
        self.assertTrue(any(map(lambda x: len(x) > 0, match)))
        
    def test_solr_all_docs(self):
        """test that our specific queries are bringing back docs"""
        responses = self.rms.batch_query(self.queries)
        self.assertTrue(any(map(lambda x: len(x) > 0, responses)))
        
    
if __name__ == "__main__":
    unittest.main()