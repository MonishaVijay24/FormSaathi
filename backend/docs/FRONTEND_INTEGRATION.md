See README section 6. Key endpoints for the existing screens:
- Profile screen: POST /api/session, POST /api/profile/documents (or /demo-load), PATCH /api/profile/fields/{key}, GET /api/profile/consistency
- Choose application: GET /api/forms
- Voice screen: POST /api/applications/start, GET .../current/question, POST .../current/answer, POST .../current/confirm
- Review screen: GET /api/applications/current/validate, PATCH /api/applications/answers/{field_id}, POST /api/profile/documents (requested evidence)
- Download screen: GET /api/export/form.pdf, GET /api/export/report.pdf, DELETE /api/session
