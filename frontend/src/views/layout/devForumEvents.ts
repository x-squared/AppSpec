export const DEV_FORUM_CAPTURE_CREATED_EVENT = 'dev-forum:capture-created';
export const DEV_FORUM_OPEN_CONTEXT_EVENT = 'dev-forum:open-context';

export interface DevForumOpenContextDetail {
  capture_url: string;
  capture_state_json: string;
  capture_gui_part?: string | null;
}
