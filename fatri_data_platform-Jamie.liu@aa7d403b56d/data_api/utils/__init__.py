import json
str = '{"a":1, "b":2}'

obj = json.dumps(str)

print(json.dumps(str))

print(json.loads(obj))

print(json.loads(json.loads(obj)))