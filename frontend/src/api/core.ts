import { ApiError } from './error';
import { recordErrorLog } from './errorLog';

const BASE = '/api';
const TOKEN_KEY = 'tpl_token';

export interface AppUser {
  id: number;
  ext_id: string;
  name: string;
  role_id: number | null;
  role_ids: number[];
  role: Code | null;
  roles: Code[];
  permissions: string[];
}

export type AppStartPage = 'my-work' | 'patients' | 'donors' | 'colloquiums' | 'coordinations' | 'reports' | 'admin' | 'e2e-tests' | 'dev-forum';

export interface UserPreferences {
  locale: 'en' | 'de';
  start_page: AppStartPage;
}

export interface HealthInfo {
  status: string;
  env?: string;
  dev_tools_enabled?: boolean;
}

export interface SupportTicketConfig {
  support_email: string;
}

export interface SupportTicketDevForumCaptureResponse {
  request_id: number;
}

export interface DevRequest {
  id: number;
  parent_request_id: number | null;
  submitter_user_id: number;
  claimed_by_user_id: number | null;
  decided_by_user_id: number | null;
  status: string;
  decision: string | null;
  capture_url: string;
  capture_gui_part: string;
  capture_state_json: string;
  request_text: string;
  developer_note_text: string | null;
  developer_response_text: string | null;
  user_review_text: string | null;
  closed_at: string | null;
  created_at: string;
  changed_at: string | null;
  updated_at: string | null;
  submitter_user: AppUser | null;
  claimed_by_user: AppUser | null;
  decided_by_user: AppUser | null;
}

export interface TranslationOverridesResponse {
  locale: string;
  entries: Record<string, string>;
}

export interface Code {
  id: number;
  type: string;
  key: string;
  pos: number;
  ext_sys: string;
  ext_key: string;
  name_default: string;
}

export interface Catalogue {
  id: number;
  type: string;
  key: string;
  pos: number;
  ext_sys: string;
  ext_key: string;
  name_default: string;
  name_en: string;
  name_de: string;
}

export interface CatalogueTypeSummary {
  type: string;
  item_count: number;
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  const token = getToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  let res: Response;
  try {
    res = await fetch(`${BASE}${path}`, { headers, ...init });
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') {
      recordErrorLog({
        source: 'http',
        message: 'The request was cancelled.',
        path,
        method: init?.method ?? 'GET',
      });
      throw new Error('The request was cancelled.');
    }
    recordErrorLog({
      source: 'http',
      message: 'Could not reach the server. Please check your connection and try again.',
      path,
      method: init?.method ?? 'GET',
    });
    throw new Error('Could not reach the server. Please check your connection and try again.');
  }
  if (!res.ok) {
    const contentType = res.headers.get('content-type') ?? '';
    let detail: unknown = null;
    if (contentType.includes('application/json')) {
      try {
        detail = await res.json();
      } catch {
        detail = null;
      }
    } else {
      detail = await res.text();
    }
    const message =
      typeof detail === 'string' && detail.trim()
        ? detail
        : `Request failed with status ${res.status}`;
    recordErrorLog({
      source: 'http',
      status: res.status,
      message,
      path,
      method: init?.method ?? 'GET',
      detail,
    });
    throw new ApiError(res.status, detail, message);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export interface MedicalValueTemplate {
  id: number;
  lab_key: string;
  kis_key: string;
  loinc_code: string | null;
  loinc_display_name: string | null;
  datatype_id: number;
  datatype: Code | null;
  datatype_def_id: number | null;
  datatype_definition: DatatypeDefinition | null;
  name_default: string;
  pos: number;
  is_main: boolean;
  medical_value_group_id: number | null;
  medical_value_group_template: MedicalValueGroup | null;
  context_templates: MedicalValueTemplateContextTemplate[];
}

export interface MedicalValueGroup {
  id: number;
  key: string;
  name_default: string;
  pos: number;
  renew_date: string | null;
  context_templates: MedicalValueGroupContextTemplate[];
}

export interface MedicalValueGroupInstance {
  id: number;
  patient_id: number;
  medical_value_group_id: number;
  medical_value_group_template: MedicalValueGroup | null;
  context_key: string;
  organ_id: number | null;
  is_donor_context: boolean;
  renew_date: string | null;
}

export interface MedicalValueGroupUpdate {
  name_default?: string;
  pos?: number;
  renew_date?: string | null;
}

export interface MedicalValueGroupContextTemplate {
  id: number;
  medical_value_group_id: number;
  context_kind: 'STATIC' | 'ORGAN' | 'DONOR' | string;
  organ_id: number | null;
  organ: Code | null;
}

export interface MedicalValueTemplateContextTemplate {
  id: number;
  medical_value_template_id: number;
  context_kind: 'STATIC' | 'ORGAN' | 'DONOR' | string;
  organ_id: number | null;
  organ: Code | null;
}

export interface DatatypeDefinition {
  id: number;
  code_id: number;
  code: Code | null;
  primitive_kind: string;
  unit: string | null;
  canonical_unit_ucum: string | null;
  allowed_units_ucum_json: string | null;
  conversion_group: string | null;
  format_pattern: string | null;
  validation_regex: string | null;
  min_value: string | null;
  max_value: string | null;
  precision: number | null;
}

export interface AccessPermission {
  id: number;
  key: string;
  name_default: string;
}

export interface AccessControlMatrix {
  roles: Code[];
  permissions: AccessPermission[];
  role_permissions: Record<string, string[]>;
}

export interface ScheduledJob {
  id: number;
  job_key: string;
  name: string;
  description: string;
  is_enabled: boolean;
  interval_seconds: number;
  next_run_at: string | null;
  max_retries: number;
  retry_delay_seconds: number;
  last_started_at: string | null;
  last_finished_at: string | null;
  last_status: string | null;
  changed_by_id: number | null;
  changed_by_user: AppUser | null;
  created_at: string;
  updated_at: string | null;
}

export interface ScheduledJobRun {
  id: number;
  job_id: number;
  trigger_type: string;
  status: string;
  attempt: number;
  correlation_id: string;
  summary: string;
  error_text: string;
  metrics_json: string;
  started_at: string;
  finished_at: string | null;
  duration_ms: number | null;
  changed_by_id: number | null;
  changed_by_user: AppUser | null;
  created_at: string;
  updated_at: string | null;
}

export interface Person {
  id: number;
  first_name: string;
  surname: string;
  user_id: string | null;
  changed_by_id: number | null;
  changed_by_user: AppUser | null;
  created_at: string;
  updated_at: string | null;
}

export interface PersonCreate {
  first_name: string;
  surname: string;
  user_id?: string | null;
}

export interface PersonUpdate {
  first_name?: string;
  surname?: string;
  user_id?: string | null;
}

export interface PersonTeam {
  id: number;
  name: string;
  members?: Person[];
  changed_by_id: number | null;
  changed_by_user: AppUser | null;
  created_at: string;
  updated_at: string | null;
}

export type ProcurementSlotKey = 'MAIN' | 'LEFT' | 'RIGHT';
export type ProcurementValueMode = 'SCALAR' | 'PERSON_SINGLE' | 'PERSON_LIST' | 'TEAM_SINGLE' | 'TEAM_LIST' | 'EPISODE';
export type ProcurementGroupDisplayLane = 'PRIMARY' | 'SECONDARY';

export interface CoordinationProcurementFieldGroupTemplate {
  id: number;
  key: string;
  name_default: string;
  comment: string;
  is_active: boolean;
  display_lane: ProcurementGroupDisplayLane;
  pos: number;
}

export interface CoordinationProcurementFieldTemplate {
  id: number;
  key: string;
  name_default: string;
  comment: string;
  is_active: boolean;
  pos: number;
  datatype_def_id: number;
  datatype_definition: DatatypeDefinition | null;
  group_template_id: number | null;
  group_template: CoordinationProcurementFieldGroupTemplate | null;
  value_mode: ProcurementValueMode;
}

export interface CoordinationProcurementFieldScopeTemplate {
  id: number;
  field_template_id: number;
  organ_id: number | null;
  organ: Code | null;
  slot_key: ProcurementSlotKey;
}

export interface CoordinationProcurementProtocolTaskGroupSelection {
  id: number;
  task_group_template_id: number;
  task_group_template: {
    id: number;
    key: string;
    name: string;
    description: string;
    scope_id: number;
    scope: Code | null;
    organ_id: number | null;
    organ: Code | null;
    is_active: boolean;
    sort_pos: number;
  } | null;
  organ_id: number | null;
  organ: Code | null;
  pos: number;
}

export interface ProcurementAdminConfig {
  field_group_templates: CoordinationProcurementFieldGroupTemplate[];
  field_templates: CoordinationProcurementFieldTemplate[];
  field_scope_templates: CoordinationProcurementFieldScopeTemplate[];
  protocol_task_group_selections: CoordinationProcurementProtocolTaskGroupSelection[];
  datatype_definitions: DatatypeDefinition[];
  organs: Code[];
}

export const authApi = {
  login: (ext_id: string) =>
    request<{ token: string; user: AppUser }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ ext_id }),
    }),
  getMe: () => request<AppUser>('/auth/me'),
  getHealth: () => request<HealthInfo>('/health'),
};

export const codesApi = {
  listCodes: (type?: string) =>
    request<Code[]>(`/codes/${type ? `?type=${encodeURIComponent(type)}` : ''}`),
  listCatalogues: (type?: string) =>
    request<Catalogue[]>(`/catalogues/${type ? `?type=${encodeURIComponent(type)}` : ''}`),
};

export const adminCatalogueApi = {
  listAdminCatalogueTypes: () =>
    request<CatalogueTypeSummary[]>('/admin/catalogues/types'),
  listAdminCatalogues: (type?: string) =>
    request<Catalogue[]>(`/admin/catalogues/${type ? `?type=${encodeURIComponent(type)}` : ''}`),
  updateAdminCatalogue: (
    id: number,
    data: Partial<Pick<Catalogue, 'pos' | 'ext_sys' | 'ext_key' | 'name_default' | 'name_en' | 'name_de'>>,
  ) =>
    request<Catalogue>(`/admin/catalogues/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
};

export const medicalValueTemplatesApi = {
  listMedicalValueTemplates: () => request<MedicalValueTemplate[]>('/medical-value-templates/'),
  getMedicalValueTemplate: (id: number) => request<MedicalValueTemplate>(`/medical-value-templates/${id}`),
};

export const medicalValueGroupsApi = {
  listMedicalValueGroups: () => request<MedicalValueGroup[]>('/medical-value-groups/'),
  updateMedicalValueGroup: (id: number, data: MedicalValueGroupUpdate) =>
    request<MedicalValueGroup>(`/medical-value-groups/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
};

export const usersApi = {
  listUsers: (roleKey?: string) =>
    request<AppUser[]>(`/users/${roleKey ? `?role_key=${encodeURIComponent(roleKey)}` : ''}`),
  getMyUserPreferences: () =>
    request<UserPreferences>('/user-preferences/me'),
  updateMyUserPreferences: (data: Partial<UserPreferences>) =>
    request<UserPreferences>('/user-preferences/me', {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
};

export const translationsApi = {
  getTranslationOverrides: (locale: string) =>
    request<TranslationOverridesResponse>(`/translations/overrides?locale=${encodeURIComponent(locale)}`),
  getAdminTranslationOverrides: (locale: string) =>
    request<TranslationOverridesResponse>(`/admin/translations/?locale=${encodeURIComponent(locale)}`),
  replaceAdminTranslationOverrides: (locale: string, entries: Record<string, string>) =>
    request<TranslationOverridesResponse>(`/admin/translations/?locale=${encodeURIComponent(locale)}`, {
      method: 'PUT',
      body: JSON.stringify({ entries }),
    }),
};

export const supportTicketApi = {
  getSupportTicketConfig: () => request<SupportTicketConfig>('/support-ticket/config'),
  captureSupportTicketInDevForum: (data: {
    capture_url: string;
    capture_gui_part: string;
    capture_state_json: string;
    request_text: string;
  }) =>
    request<SupportTicketDevForumCaptureResponse>('/support-ticket/capture-dev-forum', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

export const devForumApi = {
  createDevRequest: (data: {
    capture_url: string;
    capture_gui_part: string;
    capture_state_json: string;
    request_text: string;
  }) =>
    request<DevRequest>('/dev-forum/requests/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  getDevRequestById: (requestId: number) =>
    request<DevRequest>(`/dev-forum/requests/${requestId}`),
  listDevRequestLineage: (requestId: number) =>
    request<DevRequest[]>(`/dev-forum/requests/${requestId}/lineage`),
  listReviewDevRequests: () =>
    request<DevRequest[]>('/dev-forum/requests/review'),
  listDevelopmentDevRequests: (params?: {
    include_claimed_by_other_developers?: boolean;
    filter_claimed_by_user_id?: number | null;
  }) => {
    const query = new URLSearchParams();
    if (params?.include_claimed_by_other_developers) query.set('include_claimed_by_other_developers', 'true');
    if (typeof params?.filter_claimed_by_user_id === 'number') query.set('filter_claimed_by_user_id', String(params.filter_claimed_by_user_id));
    const suffix = query.toString();
    return request<DevRequest[]>(`/dev-forum/requests/development${suffix ? `?${suffix}` : ''}`);
  },
  claimDevRequest: (requestId: number) =>
    request<DevRequest>(`/dev-forum/requests/${requestId}/claim`, {
      method: 'POST',
    }),
  decideDevRequest: (
    requestId: number,
    data: {
      decision: 'REJECTED' | 'IMPLEMENTED';
      developer_note_text: string;
      developer_response_text: string;
    },
  ) =>
    request<DevRequest>(`/dev-forum/requests/${requestId}/decision`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  acceptDevRequestReview: (requestId: number) =>
    request<DevRequest>(`/dev-forum/requests/${requestId}/review-accept`, {
      method: 'POST',
    }),
  rejectDevRequestReview: (requestId: number, review_text: string) =>
    request<DevRequest>(`/dev-forum/requests/${requestId}/review-reject`, {
      method: 'POST',
      body: JSON.stringify({ review_text }),
    }),
};

export const adminAccessApi = {
  getAccessControlMatrix: () => request<AccessControlMatrix>('/admin/access/matrix'),
  updateRolePermissions: (roleKey: string, permissionKeys: string[]) =>
    request<AccessControlMatrix>(`/admin/access/roles/${encodeURIComponent(roleKey)}`, {
      method: 'PUT',
      body: JSON.stringify({ permission_keys: permissionKeys }),
    }),
};

export const adminSchedulerApi = {
  listScheduledJobs: () =>
    request<ScheduledJob[]>('/admin/scheduler/jobs'),
  listScheduledJobRuns: (jobKey: string, limit = 50) =>
    request<ScheduledJobRun[]>(`/admin/scheduler/jobs/${encodeURIComponent(jobKey)}/runs?limit=${limit}`),
  triggerScheduledJob: (jobKey: string, correlationId?: string) =>
    request<ScheduledJobRun>(`/admin/scheduler/jobs/${encodeURIComponent(jobKey)}/trigger`, {
      method: 'POST',
      body: JSON.stringify({ correlation_id: correlationId ?? null }),
    }),
  setScheduledJobEnabled: (jobKey: string, isEnabled: boolean) =>
    request<ScheduledJob>(`/admin/scheduler/jobs/${encodeURIComponent(jobKey)}/enabled`, {
      method: 'PUT',
      body: JSON.stringify({ is_enabled: isEnabled }),
    }),
};

export const personsApi = {
  searchPersons: (query: string) =>
    request<Person[]>(`/persons/search?query=${encodeURIComponent(query)}`),
  listTeams: () =>
    request<PersonTeam[]>('/persons/teams'),
  createPerson: (data: PersonCreate) =>
    request<Person>('/persons/', { method: 'POST', body: JSON.stringify(data) }),
};

export const adminPeopleApi = {
  listAdminPeople: (query?: string) =>
    request<Person[]>(`/admin/people/${query ? `?query=${encodeURIComponent(query)}` : ''}`),
  createAdminPerson: (data: PersonCreate) =>
    request<Person>('/admin/people/', { method: 'POST', body: JSON.stringify(data) }),
  updateAdminPerson: (id: number, data: PersonUpdate) =>
    request<Person>(`/admin/people/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  deleteAdminPerson: (id: number) =>
    request<void>(`/admin/people/${id}`, { method: 'DELETE' }),
  listPersonTeams: (includeMembers = false) =>
    request<PersonTeam[]>(`/admin/people/teams${includeMembers ? '?include_members=true' : ''}`),
  getPersonTeam: (id: number) =>
    request<PersonTeam>(`/admin/people/teams/${id}`),
  createPersonTeam: (name: string, memberIds: number[]) =>
    request<PersonTeam>('/admin/people/teams', {
      method: 'POST',
      body: JSON.stringify({ name, member_ids: memberIds }),
    }),
  updatePersonTeam: (id: number, name: string) =>
    request<PersonTeam>(`/admin/people/teams/${id}`, {
      method: 'PATCH',
      body: JSON.stringify({ name }),
    }),
  setPersonTeamMembers: (id: number, memberIds: number[]) =>
    request<PersonTeam>(`/admin/people/teams/${id}/members`, {
      method: 'PUT',
      body: JSON.stringify({ member_ids: memberIds }),
    }),
  deletePersonTeam: (id: number) =>
    request<void>(`/admin/people/teams/${id}`, { method: 'DELETE' }),
};

export const adminProcurementConfigApi = {
  getProcurementAdminConfig: () =>
    request<ProcurementAdminConfig>('/admin/procurement-config/'),
  createProcurementFieldGroupTemplate: (data: { key: string; name_default: string; comment: string; is_active?: boolean; display_lane?: ProcurementGroupDisplayLane; pos: number }) =>
    request<CoordinationProcurementFieldGroupTemplate>('/admin/procurement-config/groups', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  updateProcurementFieldGroupTemplate: (
    id: number,
    data: {
      key?: string;
      name_default?: string;
      comment?: string;
      is_active?: boolean;
      pos?: number;
      display_lane?: ProcurementGroupDisplayLane;
    },
  ) =>
    request<CoordinationProcurementFieldGroupTemplate>(`/admin/procurement-config/groups/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
  deleteProcurementFieldGroupTemplate: (id: number) =>
    request<void>(`/admin/procurement-config/groups/${id}`, { method: 'DELETE' }),
  createProcurementFieldTemplate: (data: {
    key: string;
    name_default: string;
    comment: string;
    is_active?: boolean;
    pos: number;
    datatype_def_id: number;
    group_template_id?: number | null;
    value_mode: ProcurementValueMode;
  }) =>
    request<CoordinationProcurementFieldTemplate>('/admin/procurement-config/fields', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  updateProcurementFieldTemplate: (
    id: number,
    data: {
      pos?: number;
      group_template_id?: number | null;
    },
  ) =>
    request<CoordinationProcurementFieldTemplate>(`/admin/procurement-config/fields/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
  deleteProcurementFieldTemplate: (id: number) =>
    request<void>(`/admin/procurement-config/fields/${id}`, { method: 'DELETE' }),
  createProcurementFieldScopeTemplate: (data: {
    field_template_id: number;
    organ_id?: number | null;
    slot_key: ProcurementSlotKey;
  }) =>
    request<CoordinationProcurementFieldScopeTemplate>('/admin/procurement-config/scopes', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  deleteProcurementFieldScopeTemplate: (id: number) =>
    request<void>(`/admin/procurement-config/scopes/${id}`, { method: 'DELETE' }),
  createProcurementProtocolTaskGroupSelection: (data: {
    task_group_template_id: number;
    organ_id?: number | null;
    pos?: number;
  }) =>
    request<CoordinationProcurementProtocolTaskGroupSelection>('/admin/procurement-config/protocol-task-groups', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  updateProcurementProtocolTaskGroupSelection: (
    id: number,
    data: {
      organ_id?: number | null;
      pos?: number;
    },
  ) =>
    request<CoordinationProcurementProtocolTaskGroupSelection>(`/admin/procurement-config/protocol-task-groups/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
  deleteProcurementProtocolTaskGroupSelection: (id: number) =>
    request<void>(`/admin/procurement-config/protocol-task-groups/${id}`, { method: 'DELETE' }),
};
