export interface Course {
  id: string;
  course_code: string;
  course_name: string;
}

// Backend returns an array directly, but api.md shows wrapped format
// Supporting both formats for compatibility
export type CoursesResponse = Course[] | { courses: Course[] };
