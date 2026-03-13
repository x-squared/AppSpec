# AppSpec Migration Notes

This repository contains Dev-Forum and specification-oriented capabilities extracted from TPL-App.

Included:
- Dev-Forum frontend surfaces and ticket context utilities
- Dev-Forum/support-ticket backend routes, features, and schemas
- Minimal backend model surface required by Dev-Forum/auth (`DevRequest`, `User`, `Person`, `Code`, `AccessPermission`)
- Spec and manual artifacts relevant for AppSpec ownership

Out of scope in this repository:
- TPLK clinical workflow models (patients, episodes, coordinations, tasks, procurement)
- Non-Dev-Forum runtime features that belong to AppStack/AppModules

Next step:
- replace remaining local core model copies with imports from AppStack/AppModules shared contracts
