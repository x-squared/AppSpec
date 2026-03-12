# Interface Specifications (OAS)

This folder stores OpenAPI interface specifications delivered as ZIP files.

## Structure

- `patient-interface/`
  - `incoming/` place original ZIP files here
  - `oas/` extract OpenAPI files here (`openapi.yaml`, `openapi.json`, related refs)
- `lab-interface/`
  - `incoming/` place original ZIP files here
  - `oas/` extract OpenAPI files here (`openapi.yaml`, `openapi.json`, related refs)

## Recommended workflow

1. Drop the vendor ZIP in `incoming/`.
2. Extract into `oas/` without flattening nested references.
3. Keep versioned naming for ZIPs, for example:
   - `patient-interface-v2026-03-04.zip`
   - `lab-interface-v2026-03-04.zip`

## Agent support

Yes, OAS interface specs can be processed here. Typical support includes:

- reviewing and validating paths/schemas
- comparing versions and reporting diffs
- generating client/server integration notes
- mapping endpoints to internal API contracts and tasks
