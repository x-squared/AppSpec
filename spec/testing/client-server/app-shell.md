# Client-Server Spec: Application Shell

This specification verifies that the frontend app shell is served.

```spec-case
{
  "id": "client-app-shell-renders",
  "scope": "client_server",
  "name": "Frontend root serves app shell HTML",
  "request": {
    "method": "GET",
    "path": "/"
  },
  "expect": {
    "status": 200,
    "body_contains": [
      "<!doctype html"
    ]
  }
}
```
