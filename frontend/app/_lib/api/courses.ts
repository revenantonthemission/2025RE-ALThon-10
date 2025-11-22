import { Course, CoursesResponse } from "@/app/_types/course";

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
