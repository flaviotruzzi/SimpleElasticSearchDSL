import json
import unittest
from elasticsearch import Elasticsearch
from Queries import *


TWEETS = [
    {"user": "kimchy", "post_date": "2009-11-15T14:12:12", "message": "trying out Elasticsearch"},
    {"user": "kimchy", "post_date": "2009-11-15T14:12:12", "message": "this is a test"}]


class TestQueries(unittest.TestCase):
    """docstring for TestQueries"""

    def setUp(self):
        self.es = Elasticsearch()
        self.index = "twitter"
        self.doc_type = "tweet"
        for tweet in TWEETS:
            self.es.index(self.index, "tweet", tweet)

        self.es.indices.refresh(self.index)

    def tearDown(self):
        self.es.indices.delete("twitter")

    def get_hit(self, query, hit):
        return self.search(query)["hits"]["hits"][hit]["_source"]

    def search(self, query):
        return self.es.search(self.index, self.doc_type, query.generate())

    def test_match_query(self):
        query = MatchQuery(field="message", query="this test")
        self.assertTrue(self.es.indices.validate_query(self.index, query.generate()))
        self.assertEqual(self.get_hit(query, 0), TWEETS[1])

    def test_match_all_query(self):
        query = MatchAllQuery(field="message")
        self.assertTrue(self.es.indices.validate_query(self.index, query.generate()))
        self.assertEqual(self.search(query)["hits"]["total"], len(TWEETS))

    def test_match_phrase_query(self):
        query = MatchPhraseQuery(field="message", query="this is a test")
        self.assertTrue(self.es.indices.validate_query(self.index, query.generate()))
        self.assertEqual(self.get_hit(query, 0), TWEETS[1])

        query = MatchPhraseQuery(field="message", query="not match this is a test")
        self.assertTrue(self.es.indices.validate_query(self.index, query.generate()))
        self.assertEqual(self.search(query)["hits"]["total"], 0)


if __name__ == "__main__":
    unittest.main()