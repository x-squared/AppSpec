# Architecture Specification

This directory contains formal architecture specifications for TPL-App, separated from implementation details.

## Artifacts

- `context.puml`: system context (users, app, external dependencies).
- `container.puml`: container view (frontend, backend API, database, test tooling).
- `backend-components.puml`: backend component/layer view focused on dependency direction.
- `dependency-rules.json`: machine-checkable dependency constraints for backend modules.

## Architecture dependency check

Run:

```bash
cd /Users/stephan/Workspace/TPL-App/backend
source .venv/bin/activate
cd /Users/stephan/Workspace/TPL-App
python -m qa.spec_tools.check_architecture_dependencies
```

## Maintenance rule

When architectural boundaries or dependency intent change, update this folder in the same change set as code changes.
