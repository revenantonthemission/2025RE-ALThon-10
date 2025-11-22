'use client';

import { useRouter } from 'next/navigation';
import useSWR from 'swr';
import { getCourses } from '@/app/_lib/api/courses';
import { Course } from '@/app/_types/course';
import { LandingNavbar } from '@/components/navbar';

function coursesFetcher(): Promise<Course[]> {
  return getCourses();
}

export default function CoursesPage() {
  const router = useRouter();
  const { data, error, isLoading } = useSWR<Course[]>(
    'courses',
    coursesFetcher
  );

  const handleCourseClick = (courseId: number) => {
    router.push(`/result?courseId=${courseId}`);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-base-200">
        <LandingNavbar />
        <div className="container mx-auto px-4 py-12">
          <div className="flex items-center justify-center min-h-[60vh]">
            <span className="loading loading-spinner loading-lg"></span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-base-200">
        <LandingNavbar />
        <div className="container mx-auto px-4 py-12">
          <div className="card bg-base-100 shadow-xl border border-base-300 w-full max-w-4xl mx-auto">
            <div className="card-body">
              <h2 className="card-title text-error">Error Loading Courses</h2>
              <p className="text-base-content/70">
                {error instanceof Error ? error.message : 'Failed to load courses'}
              </p>
              <div className="card-actions justify-end mt-4">
                <button
                  onClick={() => window.location.reload()}
                  className="btn btn-primary"
                >
                  Retry
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="min-h-screen bg-base-200">
        <LandingNavbar />
        <div className="container mx-auto px-4 py-12">
          <div className="card bg-base-100 shadow-xl border border-base-300 w-full max-w-4xl mx-auto">
            <div className="card-body">
              <h2 className="card-title">No Courses Found</h2>
              <p className="text-base-content/70">
                There are no courses available at the moment.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-base-200">
      <LandingNavbar />
      <div className="container mx-auto px-4 py-12">
        <div className="card bg-base-100 shadow-xl border border-base-300 w-full max-w-6xl mx-auto">
          <div className="card-body">
            <h1 className="card-title text-3xl mb-6">Course List</h1>
            <div className="divider"></div>
            <div className="overflow-x-auto">
              <table className="table table-zebra">
                <thead>
                  <tr>
                    <th>Course Code</th>
                    <th>Course Name</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((course) => (
                    <tr
                      key={course.id}
                      onClick={() => handleCourseClick(course.id)}
                      className="cursor-pointer hover:bg-base-200 transition-colors"
                    >
                      <td className="font-mono font-semibold">
                        {course.course_code}
                      </td>
                      <td>{course.course_name}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="divider"></div>
            <div className="text-sm text-base-content/70">
              Total: {data.length} course{data.length !== 1 ? 's' : ''}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

