export interface ClientErrorLogEntry {
  ts: string;
  source: 'http' | 'ui';
  message: string;
  status?: number;
  path?: string;
  method?: string;
  detail?: unknown;
}

const MAX_ERROR_LOG_ENTRIES = 200;
const errorLog: ClientErrorLogEntry[] = [];

export function recordErrorLog(entry: Omit<ClientErrorLogEntry, 'ts'>): void {
  errorLog.push({
    ts: new Date().toISOString(),
    ...entry,
  });
  if (errorLog.length > MAX_ERROR_LOG_ENTRIES) {
    errorLog.splice(0, errorLog.length - MAX_ERROR_LOG_ENTRIES);
  }
}

export function getRecentErrorLog(limit = 40): ClientErrorLogEntry[] {
  if (limit <= 0) return [];
  return errorLog.slice(-limit);
}

