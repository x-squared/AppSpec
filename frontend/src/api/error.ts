import { recordErrorLog } from './errorLog';

export class ApiError extends Error {
  status: number;
  detail: unknown;

  constructor(status: number, detail: unknown, message: string) {
    super(message);
    this.status = status;
    this.detail = detail;
  }
}

interface FastApiValidationErrorItem {
  loc?: Array<string | number>;
  msg?: string;
}

function statusFallback(status: number): string {
  if (status === 400) return 'The request is invalid.';
  if (status === 401) return 'Your session has expired. Please log in again.';
  if (status === 403) return 'You are not allowed to perform this action.';
  if (status === 404) return 'The requested resource was not found.';
  if (status === 409) return 'Data was changed in another window/session. Reload and try again.';
  if (status === 422) return 'Please correct the input values.';
  if (status >= 500) return 'The server reported an internal error. Please try again.';
  return 'The request failed. Please try again.';
}

function formatValidationMessage(item: FastApiValidationErrorItem): string {
  const loc = item.loc ?? [];
  const fieldPath = loc
    .filter((segment) => !['body', 'query', 'path'].includes(String(segment)))
    .map(String)
    .join('.');
  const rawMessage = (item.msg ?? 'Invalid value').replace(/^Value error,\s*/i, '');
  return fieldPath ? `${fieldPath}: ${rawMessage}` : rawMessage;
}

function listDetailMessages(detail: unknown): string[] {
  if (!Array.isArray(detail)) return [];
  return (detail as FastApiValidationErrorItem[])
    .map(formatValidationMessage)
    .filter((msg) => msg.length > 0);
}

function describeApiError(error: ApiError, fallback: string): string {
  const wrappedDetail = (error.detail as { detail?: unknown })?.detail;
  const details = listDetailMessages(wrappedDetail);
  if (details.length > 0) {
    if (error.status === 422) {
      return `Please correct the input: ${details.join(' | ')}`;
    }
    return details.join(' | ');
  }
  if (typeof wrappedDetail === 'string' && wrappedDetail.trim()) {
    return wrappedDetail;
  }
  if (typeof error.detail === 'string' && error.detail.trim()) {
    return error.detail;
  }
  if (error.message.trim() && !/^request failed with status \d+$/i.test(error.message.trim())) {
    return error.message;
  }
  if (error.status > 0) {
    return statusFallback(error.status);
  }
  return fallback;
}

function describeGenericError(error: Error, fallback: string): string {
  if (error.name === 'AbortError') {
    return 'The request was cancelled.';
  }
  if (error.name === 'TypeError') {
    return 'Could not reach the server. Please check your connection and try again.';
  }
  if (error.message.trim()) {
    return error.message;
  }
  return fallback;
}

export function toUserErrorMessage(error: unknown, fallback: string): string {
  let resolved = fallback;
  if (error instanceof ApiError) {
    resolved = describeApiError(error, fallback);
    recordErrorLog({
      source: 'ui',
      message: resolved,
      status: error.status,
      detail: error.detail,
    });
    return resolved;
  }
  if (error instanceof Error) {
    resolved = describeGenericError(error, fallback);
    recordErrorLog({
      source: 'ui',
      message: resolved,
      detail: error.message,
    });
    return resolved;
  }
  recordErrorLog({
    source: 'ui',
    message: fallback,
    detail: error,
  });
  return fallback;
}

