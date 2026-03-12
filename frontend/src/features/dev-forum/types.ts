export type DevForumTabKey = 'capturing' | 'review' | 'development';

export interface SelectedComponentDescriptor {
  selector: string;
  tag: string;
  id: string;
  class_name: string;
  text_sample: string;
}

export interface CapturedContextPayload {
  capture_url: string;
  capture_gui_part: string;
  capture_state_json: string;
}
