## MatchQuery

Create a simple MatchQuery. It accept the following parameters: 
```python
['field', 'query', 'operator', 'minimum_should_match','analyzer', 'fuzziness',
 'prefix_length', 'max_expansions', 'zero_terms_query', 'cutoff_frequency']
```
### Examples
```python
query = MatchQuery(field="message", query="this is a test", analyzer="standard")

print json.dumps(query.generate(), sort_keys=True, indent=2)
```
```json
{
  "query": {
    "match": {
      "message": {
        "query": "this is a test"
      }
    }
  }
}
```
```python
query = MatchQuery(field="message", query="this is a test", operator="and")

print json.dumps(query.generate(), sort_keys=True, indent=2)
```
```json
{
  "query": {
    "match": {
      "message": {
        "operator": "and", 
        "query": "this is a test"
      }
    }
  }
}
```
```python
query = MatchQuery(field="message", query="this is a test", operator="and", 
                   "zero_terms_query"="all")

print json.dumps(query.generate(), sort_keys=True, indent=2)
```
```json
{
  "query": {
    "match": {
      "message": {
        "operator": "and", 
        "query": "to be or not to be", 
        "zero_terms_query": "all"
      }
    }
  }
}
```
