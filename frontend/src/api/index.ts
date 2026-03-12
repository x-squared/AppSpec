export { getToken, setToken, clearToken, authApi, codesApi, medicalValueTemplatesApi, medicalValueGroupsApi, usersApi, translationsApi, adminAccessApi, adminSchedulerApi, personsApi, adminPeopleApi, adminProcurementConfigApi, adminCatalogueApi, supportTicketApi, devForumApi } from './core';
export type {
  AppUser,
  AccessControlMatrix,
  AccessPermission,
  ScheduledJob,
  ScheduledJobRun,
  Person,
  PersonCreate,
  PersonUpdate,
  PersonTeam,
  Code,
  Catalogue,
  CatalogueTypeSummary,
  HealthInfo,
  SupportTicketConfig,
  SupportTicketDevForumCaptureResponse,
  DevRequest,
  TranslationOverridesResponse,
  UserPreferences,
  AppStartPage,
  DatatypeDefinition,
  ProcurementGroupDisplayLane,
  ProcurementSlotKey,
  ProcurementValueMode,
  CoordinationProcurementFieldGroupTemplate,
  CoordinationProcurementFieldTemplate,
  CoordinationProcurementFieldScopeTemplate,
  ProcurementAdminConfig,
  MedicalValueGroupInstance,
  MedicalValueTemplate,
  MedicalValueGroup,
  MedicalValueGroupUpdate,
} from './core';

export { patientsApi } from './patients';
export type {
  ContactInfo, ContactInfoCreate, ContactInfoUpdate,
  Absence, AbsenceCreate, AbsenceUpdate,
  Diagnosis, DiagnosisCreate, DiagnosisUpdate,
  MedicalValue, MedicalValueCreate, MedicalValueUpdate,
  Episode, EpisodeCreate, EpisodeUpdate, EpisodeOrgan, EpisodeOrganCreate, EpisodeOrganUpdate,
  Patient, PatientListItem, PatientCreate, PatientUpdate,
} from './patients';
export { tasksApi } from './tasks';
export type {
  EnsureCoordinationProtocolTaskGroupsResponse,
  Task,
  TaskCreate,
  TaskKindKey,
  TaskGroup,
  TaskGroupCreate,
  TaskGroupListParams,
  TaskGroupTemplate,
  TaskGroupTemplateCreate,
  TaskGroupTemplateUpdate,
  TaskGroupUpdate,
  TaskListParams,
  TaskTemplate,
  TaskTemplateCreate,
  TaskTemplateListParams,
  TaskTemplateUpdate,
  TaskUpdate,
} from './tasks';
export { colloqiumsApi } from './colloqiums';
export type {
  Colloqium,
  ColloqiumAgenda,
  ColloqiumAgendaCreate,
  ColloqiumAgendaUpdate,
  ColloqiumCreate,
  ColloqiumTypeUpdate,
  ColloqiumUpdate,
  ColloqiumType,
} from './colloqiums';
export { coordinationsApi } from './coordinations';
export type {
  Coordination,
  CoordinationCreate,
  CoordinationUpdate,
  CoordinationDonor,
  CoordinationDonorUpsert,
  CoordinationOrigin,
  CoordinationOriginUpsert,
  CoordinationTimeLog,
  CoordinationTimeLogCreate,
  CoordinationTimeLogUpdate,
  CoordinationCompletionState,
  CoordinationCompletionTaskGroup,
  CoordinationProtocolEventLog,
  CoordinationProtocolEventLogCreate,
  CoordinationEpisode,
  CoordinationEpisodeLinkedEpisode,
  CoordinationProtocolState,
  CoordinationProtocolStateOrgan,
  CoordinationProtocolStateSlot,
  CoordinationProcurementFlex,
  CoordinationProcurementValue,
  CoordinationProcurementValueUpsert,
} from './coordinations';
export { favoritesApi } from './favorites';
export type { Favorite, FavoriteCreate, FavoriteTypeKey } from './favorites';
export { informationApi } from './information';
export type { Information, InformationCreate, InformationUpdate } from './information';
export { reportsApi } from './reports';
export type {
  ReportSourceKey,
  ReportValueType,
  ReportOperatorKey,
  ReportSortDirection,
  ReportFieldOption,
  ReportJoinOption,
  ReportSourceOption,
  ReportMetadataResponse,
  ReportFilterInput,
  ReportSortInput,
  ReportExecuteRequest,
  ReportColumn,
  ReportExecuteResponse,
} from './reports';
export { e2eTestsApi } from './e2eTests';
export type {
  E2ETestCaseResult,
  E2ETestRunnerKey,
  E2ETestRunnerOption,
  E2ETestMetadataResponse,
  E2ETestRunRequest,
  E2ETestRunResponse,
} from './e2eTests';

import { authApi, codesApi, medicalValueTemplatesApi, medicalValueGroupsApi, usersApi, translationsApi, adminAccessApi, adminSchedulerApi, personsApi, adminPeopleApi, adminProcurementConfigApi, adminCatalogueApi, supportTicketApi, devForumApi } from './core';
import { patientsApi } from './patients';
import { tasksApi } from './tasks';
import { colloqiumsApi } from './colloqiums';
import { coordinationsApi } from './coordinations';
import { favoritesApi } from './favorites';
import { informationApi } from './information';
import { reportsApi } from './reports';
import { e2eTestsApi } from './e2eTests';

export const api = {
  ...authApi,
  ...codesApi,
  ...medicalValueTemplatesApi,
  ...medicalValueGroupsApi,
  ...usersApi,
  ...translationsApi,
  ...adminAccessApi,
  ...adminSchedulerApi,
  ...personsApi,
  ...adminPeopleApi,
  ...adminProcurementConfigApi,
  ...adminCatalogueApi,
  ...supportTicketApi,
  ...devForumApi,
  ...patientsApi,
  ...tasksApi,
  ...colloqiumsApi,
  ...coordinationsApi,
  ...favoritesApi,
  ...informationApi,
  ...reportsApi,
  ...e2eTestsApi,
};
