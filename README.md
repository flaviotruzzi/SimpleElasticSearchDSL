## MatchQuery

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
