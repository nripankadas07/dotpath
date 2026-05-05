# dotpath

Dotted-key get/set/has/del over nested dicts and lists. Zero deps.

```python
from dotpath import get, set_, has, delete, paths

d = {"users": [{"name": "alice"}, {"name": "bob"}]}
get(d, "users.1.name")            # 'bob'
get(d, "users.5.name", default=None)  # None

set_(d, "users.0.email", "a@x")
# {"users": [{"name": "alice", "email": "a@x"}, {"name": "bob"}]}

has(d, "users.0.email")           # True
delete(d, "users.0.email")
list(paths(d))                     # ['users.0.name', 'users.1.name']
```

`\\.` escapes a literal dot inside a key segment. List indices are
integers; negatives count from the end.

MIT.
