# Conceptual Domain Consistency

This conceptual test verifies that the intent-level domain model still matches backend SQLAlchemy model structures.

```conceptual-case
{
  "id": "domain-database-consistency",
  "name": "Conceptual model and SQLAlchemy model stay aligned",
  "checker": "domain_database_sync",
  "diagram": "spec/domain/gen-domain.puml",
  "mapping": "spec/domain/domain-sync-mapping.json"
}
```
