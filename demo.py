__author__ = 'ftruzzi'
import json
from Queries import *

query = MatchQuery(field="message", query="this is a test", analyzer="standard")

print json.dumps(query.generate(), sort_keys=True, indent=2)

query = MatchQuery(field="message", query="this is a test", operator="and")

print json.dumps(query.generate(), sort_keys=True, indent=2)

query = MatchQuery(field="message", query="to be or not to be", operator="and",
                   zero_terms_query="all")

print json.dumps(query.generate(), sort_keys=True, indent=2)