# Server Spec: Health Endpoint

This specification captures baseline backend availability.

```spec-case
{
  "id": "server-health-ok",
  "scope": "server",
  "name": "Health endpoint returns OK status",
  "request": {
    "method": "GET",
    "path": "/api/health"
  },
  "expect": {
    "status": 200,
    "json_subset": {
      "status": "ok"
    }
  }
}
```
