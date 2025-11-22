export interface Course {
  id: number;
  course_code: string;
  course_name: string;
}

// Backend returns an array directly, but api.md shows wrapped format
// Supporting both formats for compatibility
export type CoursesResponse = Course[] | { courses: Course[] };

// Course evaluation types
export interface CourseHistory {
  course_id: string;
  grade: string;
}

export interface UserProfile {
  taken_courses: CourseHistory[];
  eval_preference: number; // 1: exam preference ~ 5: assignment preference
  interests: string[];
  team_preference: number; // 1: strongly dislike ~ 5: strongly like
  attendence_type: string[]; // e.g., ["online", "offline", "hybrid"]
}

export interface AnalysisDetail {
  criteria: string;
  score: number; // 1-5 suitability score
  reason: string;
}

export interface CourseEvaluationResponse {
  course_id: string;
  details: AnalysisDetail[];
  summary: string;
  recommendation?: number | null; // Recommended course ID (optional)
}
