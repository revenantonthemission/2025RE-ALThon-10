'use client';

import { Suspense, useMemo, useEffect, useState, useRef } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { RadarChart, type RadarChartData } from './_components/radar-chart';
import { CourseResultTile, type CourseInfo } from './_components/course-result-tile';
import { usePreferencesStore } from '@/app/_stores/preferences';
import { evaluateCourse, getCourses } from '@/app/_lib/api/courses';
import type {
  CourseEvaluationResponse,
  UserProfile,
  AnalysisDetail,
} from '@/app/_types/course';
import type { Course } from '@/app/_types/course';

function ResultContent() {
  const searchParams = useSearchParams();
  const courseIdParam = searchParams.get('courseId');
  const courseId = courseIdParam ? parseInt(courseIdParam, 10) : null;

  const preferences = usePreferencesStore((state) => state.preferences);
  const queryClient = useQueryClient();
  const [course, setCourse] = useState<Course | null>(null);

  // Build userProfile from preferences
  const userProfile: UserProfile | null = preferences
    ? {
        taken_courses: preferences.completed_courses.map(c => ({
          course_id: c.id,
          grade: c.grade,
        })),
        eval_preference: preferences.eval_preference,
        interests: preferences.interests.map(i => i.value),
        team_preference: preferences.team_preference,
        attendence_type: preferences.class_type,
      }
    : null;

  // Fetch course evaluation using React Query
  const {
    data: evaluation,
    isLoading,
    error: queryError,
  } = useQuery<CourseEvaluationResponse>({
    queryKey: ['evaluate-course', courseId],
    queryFn: async () => {
      if (!courseId || !userProfile) {
        throw new Error('Course ID and preferences are required');
      }
      return evaluateCourse(courseId, userProfile);
    },
    enabled: !!courseId && !!userProfile,
    // Use default options from QueryClient (staleTime: Infinity, refetchOnMount: false)
  });

  // Fetch course details
  useEffect(() => {
    if (!courseId) return;

    const fetchCourse = async () => {
      try {
        const courses = await getCourses();
        const foundCourse = courses.find(c => c.id === courseId);
        if (foundCourse) {
          setCourse(foundCourse);
        }
      } catch (err) {
        // Silently handle error - course display is not critical
        console.error('Failed to fetch course details:', err);
      }
    };

    fetchCourse();
  }, [courseId]);

  // Invalidate cache when preferences change
  const prevPreferencesRef = useRef(preferences);
  useEffect(() => {
    // Only invalidate if preferences actually changed
    if (preferences && prevPreferencesRef.current !== preferences) {
      queryClient.invalidateQueries({ queryKey: ['evaluate-course'] });
      prevPreferencesRef.current = preferences;
    }
  }, [preferences, queryClient]);

  // Convert query error to string for display
  const error = queryError
    ? queryError instanceof Error
      ? queryError.message
      : 'Failed to evaluate course'
    : null;

  // Generate chart data from evaluation results
  const chartData = useMemo<RadarChartData | null>(() => {
    if (!evaluation || !evaluation.details) return null;

    // Use evaluation details to create radar chart
    return {
      labels: evaluation.details.map((detail: AnalysisDetail) => detail.criteria),
      datasets: [
        {
          label: 'Suitability Score',
          data: evaluation.details.map((detail: AnalysisDetail) => (detail.score / 5) * 100), // Convert 1-5 scale to 0-100
        },
      ],
    };
  }, [evaluation]);

  // Fallback chart data from preferences (when no courseId)
  const preferenceChartData = useMemo<RadarChartData | null>(() => {
    if (!preferences || courseId) return null;

    return {
      labels: [
        'Evaluation Preference',
        'Team Preference',
        'Interests Count',
        'Class Type Count',
        'Engagement Level',
        'Collaboration',
      ],
      datasets: [
        {
          label: 'Your Profile',
          data: [
            (preferences.eval_preference / 5) * 100,
            (preferences.team_preference / 5) * 100,
            Math.min((preferences.interests?.length || 0) * 20, 100),
            Math.min((preferences.class_type?.length || 0) * 33.33, 100),
            ((preferences.eval_preference + preferences.team_preference) / 10) * 100,
            (preferences.team_preference / 5) * 100,
          ],
        },
      ],
    };
  }, [preferences, courseId]);

  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-base-200 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="card bg-base-100 shadow-xl border border-base-300 w-full max-w-3xl mx-auto">
          <div className="card-body">
            <div className="flex items-center justify-center">
              <span className="loading loading-spinner loading-lg"></span>
            </div>
            <p className="text-center text-base-content/70 mt-4">
              Evaluating course...
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="min-h-screen bg-base-200 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="card bg-base-100 shadow-xl border border-base-300 w-full max-w-3xl mx-auto">
          <div className="card-body">
            <h2 className="card-title text-error text-2xl mb-4">Error</h2>
            <p className="text-base-content/70 mb-4">{error}</p>
            <div className="card-actions">
              <Link href="/courses" className="btn btn-outline">
                Back to Courses
              </Link>
              <Link href="/preference" className="btn btn-primary">
                Go to Preferences
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // No preferences state
  if (!preferences) {
    return (
      <div className="min-h-screen bg-base-200 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="card bg-base-100 shadow-xl border border-base-300 w-full max-w-3xl mx-auto">
          <div className="card-body">
            <h2 className="card-title text-2xl mb-4">No Preferences Found</h2>
            <p className="text-base-content/70 mb-4">
              Please complete the preference form first to see your results.
            </p>
            <div className="card-actions">
              <Link href="/preference" className="btn btn-primary">
                Go to Preferences
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Course evaluation view
  if (courseId && course && evaluation) {
    const courseInfo: CourseInfo = {
      course_code: course.course_code,
      course_name: course.course_name,
    };

    // Calculate average match score
    const avgScore = evaluation.details.length > 0
      ? evaluation.details.reduce((sum: number, d: AnalysisDetail) => sum + d.score, 0) / evaluation.details.length
      : 0;
    const matchScore = (avgScore / 5) * 100;

    return (
      <div className="min-h-screen bg-base-200 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto space-y-8">
          {/* Course Evaluation Result */}
          {chartData && (
            <CourseResultTile
              course={courseInfo}
              chartData={chartData}
              chartTitle="Course Suitability Analysis"
              matchScore={matchScore}
              description={evaluation.summary}
            />
          )}

          {/* Evaluation Details */}
          {evaluation.details && evaluation.details.length > 0 && (
            <div className="card bg-base-100 shadow-xl border border-base-300">
              <div className="card-body">
                <h2 className="card-title text-2xl mb-4">Evaluation Details</h2>
                <div className="space-y-4">
                  {evaluation.details.map((detail: AnalysisDetail, index: number) => (
                    <div key={index} className="card bg-base-200 border border-base-300">
                      <div className="card-body">
                        <div className="flex flex-col items-start justify-between gap-4">
                          <div className="flex-1">
                            <h3 className="font-semibold text-lg mb-2">
                              {detail.criteria}
                            </h3>
                            <p className="text-base-content/70">{detail.reason}</p>
                          </div>
                          <div className="stat bg-base-100 rounded-lg p-4 min-w-[100px]">
                            <div className="stat-title text-xs">Score</div>
                            <div className="stat-value text-2xl text-primary">
                              {detail.score}/5
                            </div>
                          </div>
                        </div>
                        <progress
                          className="progress progress-primary w-full mt-2"
                          value={(detail.score / 5) * 100}
                          max="100"
                        ></progress>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="card bg-base-100 shadow-xl border border-base-300">
            <div className="card-body">
              <div className="card-actions justify-end">
                <Link href="/courses" className="btn btn-outline">
                  Back to Courses
                </Link>
                <Link href="/preference" className="btn btn-outline">
                  Edit Preferences
                </Link>
                <Link href="/" className="btn btn-primary">
                  Back to Home
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Fallback to preference view (no courseId)
  if (!preferenceChartData) {
    return (
      <div className="min-h-screen bg-base-200 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="card bg-base-100 shadow-xl border border-base-300 w-full max-w-3xl mx-auto">
          <div className="card-body">
            <h2 className="card-title text-2xl mb-4">No Data Available</h2>
            <p className="text-base-content/70 mb-4">
              Please select a course from the courses page or complete your preferences.
            </p>
            <div className="card-actions">
              <Link href="/courses" className="btn btn-primary">
                View Courses
              </Link>
              <Link href="/preference" className="btn btn-outline">
                Go to Preferences
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Default preference view (no courseId)
  return (
    <div className="min-h-screen bg-base-200 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header Card */}
        <div className="card bg-base-100 shadow-xl border border-base-300">
          <div className="card-body">
            <h1 className="card-title text-3xl mb-2">Your Learning Profile</h1>
            <p className="text-base-content/70">
              Visual representation of your preferences and learning style
            </p>
          </div>
        </div>

        {/* Radar Chart Card */}
        <div className="card bg-base-100 shadow-xl border border-base-300">
          <div className="card-body">
            <RadarChart data={preferenceChartData} title="Preference Analysis" />
          </div>
        </div>

        {/* Details Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Evaluation Preference */}
          <div className="card bg-base-100 shadow-xl border border-base-300">
            <div className="card-body">
              <h2 className="card-title text-xl">Evaluation Preference</h2>
              <div className="stat">
                <div className="stat-value text-primary">
                  {preferences.eval_preference}/5
                </div>
                <div className="stat-desc">Your preferred evaluation style</div>
              </div>
              <progress
                className="progress progress-primary w-full"
                value={(preferences.eval_preference / 5) * 100}
                max="100"
              ></progress>
            </div>
          </div>

          {/* Team Preference */}
          <div className="card bg-base-100 shadow-xl border border-base-300">
            <div className="card-body">
              <h2 className="card-title text-xl">Team Preference</h2>
              <div className="stat">
                <div className="stat-value text-secondary">
                  {preferences.team_preference}/5
                </div>
                <div className="stat-desc">Your team collaboration preference</div>
              </div>
              <progress
                className="progress progress-secondary w-full"
                value={(preferences.team_preference / 5) * 100}
                max="100"
              ></progress>
            </div>
          </div>

          {/* Interests */}
          <div className="card bg-base-100 shadow-xl border border-base-300">
            <div className="card-body">
              <h2 className="card-title text-xl">Interests</h2>
              <div className="stat">
                <div className="stat-value text-accent">
                  {preferences.interests?.length || 0}
                </div>
                <div className="stat-desc">Number of interests selected</div>
              </div>
              <div className="flex flex-wrap gap-2 mt-4">
                {preferences.interests?.map((interest, index) => (
                  <div key={index} className="badge badge-accent badge-lg">
                    {interest.value}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Class Types */}
          <div className="card bg-base-100 shadow-xl border border-base-300">
            <div className="card-body">
              <h2 className="card-title text-xl">Class Types</h2>
              <div className="stat">
                <div className="stat-value text-info">
                  {preferences.class_type?.length || 0}
                </div>
                <div className="stat-desc">Number of class types selected</div>
              </div>
              <div className="flex flex-wrap gap-2 mt-4">
                {preferences.class_type?.map((type, index) => (
                  <div key={index} className="badge badge-info badge-lg">
                    {type}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="card bg-base-100 shadow-xl border border-base-300">
          <div className="card-body">
            <div className="card-actions justify-end">
              <Link href="/preference" className="btn btn-outline">
                Edit Preferences
              </Link>
              <Link href="/" className="btn btn-primary">
                Back to Home
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ResultPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-base-200 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
          <div className="card bg-base-100 shadow-xl border border-base-300 w-full max-w-3xl mx-auto">
            <div className="card-body">
              <div className="flex items-center justify-center">
                <span className="loading loading-spinner loading-lg"></span>
              </div>
              <p className="text-center text-base-content/70 mt-4">
                Loading...
              </p>
            </div>
          </div>
        </div>
      }
    >
      <ResultContent />
    </Suspense>
  );
}

