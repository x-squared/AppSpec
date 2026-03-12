# Client-Server Spec: Create Patient From Recipients View

This scenario verifies a real user flow:

1. Open the application
2. Log in
3. Open Recipients/Patients view
4. Create a new patient via UI
5. Verify the patient appears in UI
6. Verify the patient exists in the database

```partner-case
{
  "id": "partner-create-patient-ui-db",
  "scope": "client_server_partner",
  "name": "Create patient via Recipients view and verify DB persistence",
  "ui_flow": {
    "login_ext_id": "TKOORD",
    "open_recipients_view": true,
    "create_patient": {
      "pid_prefix": "AUTO",
      "first_name": "Spec",
      "name": "Patient",
      "date_of_birth": "1990-01-01"
    }
  },
  "verify": {
    "ui_contains_created_pid": true,
    "database_contains_created_patient": true
  }
}
```
