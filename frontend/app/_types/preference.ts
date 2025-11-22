/**
 * User preferences stored in localStorage
 * This type matches the form data structure from the preference form
 */
export interface UserPreferences {
  eval_preference: number;
  example_interests: Array<{
    id: string;
    value: string;
    checked?: boolean;
  }>;
  interests: Array<{ value: string }>;
  team_preference: number;
  class_type: string[];
  completed_courses: Array<{
    id: string;
    grade: string;
  }>;
}
