from fastapi import FastAPI

from . import (
    absences,
    admin_access,
    admin_catalogues,
    admin_scheduler,
    admin_translations,
    admin_procurement_config,
    admin_people,
    auth,
    catalogues,
    e2e_tests,
    dev_forum,
    colloqium_agendas,
    colloqium_types,
    colloqiums,
    coordination_donors,
    coordination_episodes,
    coordination_organ_effects,
    coordination_protocol_state,
    coordination_protocol_events,
    coordination_procurements,
    coordination_procurement_flex,
    coordination_time_logs,
    coordination_origins,
    coordinations,
    codes,
    contact_infos,
    diagnoses,
    episodes,
    favorites,
    information,
    medical_data,
    medical_value_groups,
    medical_values,
    persons,
    patients,
    reports_router as reports,
    task_group_templates,
    task_groups,
    task_templates,
    tasks,
    translations,
    support_ticket,
    user_preferences,
    users,
)


def register_routers(app: FastAPI) -> None:
    """Register all API routers."""
    app.include_router(auth.router, prefix="/api")
    app.include_router(admin_access.router, prefix="/api")
    app.include_router(admin_catalogues.router, prefix="/api")
    app.include_router(admin_scheduler.router, prefix="/api")
    app.include_router(admin_translations.router, prefix="/api")
    app.include_router(admin_procurement_config.router, prefix="/api")
    app.include_router(admin_people.router, prefix="/api")
    app.include_router(e2e_tests.router, prefix="/api")
    app.include_router(dev_forum.router, prefix="/api")
    app.include_router(patients.router, prefix="/api")
    app.include_router(reports.router, prefix="/api")
    app.include_router(contact_infos.router, prefix="/api")
    app.include_router(absences.router, prefix="/api")
    app.include_router(diagnoses.router, prefix="/api")
    app.include_router(episodes.router, prefix="/api")
    app.include_router(favorites.router, prefix="/api")
    app.include_router(information.router, prefix="/api")
    app.include_router(medical_data.router, prefix="/api")
    app.include_router(medical_value_groups.router, prefix="/api")
    app.include_router(medical_values.router, prefix="/api")
    app.include_router(persons.router, prefix="/api")
    app.include_router(codes.router, prefix="/api")
    app.include_router(catalogues.router, prefix="/api")
    app.include_router(users.router, prefix="/api")
    app.include_router(colloqium_types.router, prefix="/api")
    app.include_router(colloqiums.router, prefix="/api")
    app.include_router(colloqium_agendas.router, prefix="/api")
    app.include_router(coordinations.router, prefix="/api")
    app.include_router(coordination_donors.router, prefix="/api")
    app.include_router(coordination_episodes.router, prefix="/api")
    app.include_router(coordination_organ_effects.router, prefix="/api")
    app.include_router(coordination_protocol_state.router, prefix="/api")
    app.include_router(coordination_protocol_events.router, prefix="/api")
    app.include_router(coordination_procurements.router, prefix="/api")
    app.include_router(coordination_procurement_flex.router, prefix="/api")
    app.include_router(coordination_time_logs.router, prefix="/api")
    app.include_router(coordination_origins.router, prefix="/api")
    app.include_router(task_group_templates.router, prefix="/api")
    app.include_router(task_groups.router, prefix="/api")
    app.include_router(task_templates.router, prefix="/api")
    app.include_router(tasks.router, prefix="/api")
    app.include_router(translations.router, prefix="/api")
    app.include_router(support_ticket.router, prefix="/api")
    app.include_router(user_preferences.router, prefix="/api")
