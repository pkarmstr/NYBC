#!/usr/bin/python
# -*- coding: UTF-8 -*-

import codecs
import unittest
from yiddish_solr import RednMitSolr

class SolrYiddishTest(unittest.TestCase):
    """a simple test suite to check that my connection with Solr is executing 
    queries correctly and returning results
    
    """
    
    def setUp(self):
        self.rms = RednMitSolr("http://localhost:8983/solr")
        self.yiddish_queries = map(codecs.decode,\
                                   ["לעצט", "ברודער", "קאמוניזם"])
    
    def test_simple(self):
        """make sure we can handle a simple single query"""
        resp = self.rms.connection.search(self.yiddish_queries[0], rows=50)
        self.assertGreater(len(resp.docs), 0)
            
    def test_get_all_docs(self):
        """making sure we have access to all of the doocuments"""
        resp = self.rms.connection.search("*:*", rows=100)
        self.assertEqual(len(resp.docs), 49)
            
    def test_batch_query(self):
        """see if the class function works properly"""
        self.resp = self.rms.batch_query(self.yiddish_queries)
        self.assertEqual(len(self.resp), 3)
        
    
if __name__ == "__main__":
    unittest.main()