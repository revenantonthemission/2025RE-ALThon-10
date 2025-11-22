import {
  Course,
  CoursesResponse,
  UserProfile,
  CourseEvaluationResponse,
} from "@/app/_types/course";

// Use empty string for relative URLs (same origin as Next.js)
// Set NEXT_PUBLIC_API_URL="" to use same origin, or set full URL for different origin
const API_URL = process.env.NEXT_PUBLIC_API_URL || "/api";

/**
 * Fetches the list of courses from the server
 * Backend returns an array directly, but we normalize it to always return Course[]
 */
export async function getCourses(): Promise<Course[]> {
  const response = await fetch(`${API_URL}/courses`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      error: "Failed to fetch courses",
    }));
    throw new Error(error.error || "Failed to fetch courses");
  }

  const data: CoursesResponse = await response.json();

  // Handle both array and wrapped object formats
  if (Array.isArray(data)) {
    return data;
  }

  return data.courses || [];
}

/**
 * Evaluates a course for a specific user profile using Gemini AI
 * @param courseId - The ID of the course to evaluate
 * @param userProfile - User's profile including course history and preferences
 * @returns Course evaluation response with details and summary
 * @throws Error if the course is not found or the request fails
 */
export async function evaluateCourse(
  courseId: number,
  userProfile: UserProfile
): Promise<CourseEvaluationResponse> {
  const response = await fetch(`${API_URL}/courses/${courseId}/evaluate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userProfile),
  });

  if (!response.ok) {
    if (response.status === 404) {
      const error = await response.json().catch(() => ({
        detail: "Course not found",
      }));
      throw new Error(error.detail || "Course not found");
    }

    const error = await response.json().catch(() => ({
      error: "Failed to evaluate course",
    }));
    throw new Error(error.detail || error.error || "Failed to evaluate course");
  }

  const data: CourseEvaluationResponse = await response.json();
  return data;
}
