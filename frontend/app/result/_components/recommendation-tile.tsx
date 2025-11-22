'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { getCourses } from '@/app/_lib/api/courses';
import type { Course } from '@/app/_types/course';

/**
 * Props for the RecommendationTile component
 */
interface RecommendationTileProps {
  /** Recommended course ID */
  recommendedCourseId: number | null;
}

/**
 * RecommendationTile Component
 * 
 * Displays a recommended course based on similar users' course history.
 * Shows course information and provides a link to evaluate the recommended course.
 * 
 * Features:
 * - Fetches and displays recommended course details
 * - Shows course code, name, and metadata
 * - Provides action button to evaluate the recommended course
 * - Handles loading and error states gracefully
 * 
 * @param props - Component props containing the recommended course ID
 * @returns JSX element representing the recommendation tile
 */
export function RecommendationTile({ recommendedCourseId }: RecommendationTileProps) {
  const [recommendedCourse, setRecommendedCourse] = useState<Course | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!recommendedCourseId) {
      return;
    }

    const fetchRecommendedCourse = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const courses = await getCourses();
        const foundCourse = courses.find(c => c.id === recommendedCourseId);
        if (foundCourse) {
          setRecommendedCourse(foundCourse);
        } else {
          setError('Recommended course not found');
        }
      } catch (err) {
        console.error('Failed to fetch recommended course:', err);
        setError('Failed to load recommended course');
      } finally {
        setIsLoading(false);
      }
    };

    fetchRecommendedCourse();
  }, [recommendedCourseId]);

  // Don't render if no recommendation
  if (!recommendedCourseId) {
    return null;
  }

  // Loading state
  if (isLoading) {
    return (
      <div className="card bg-base-100 shadow-xl border border-base-300">
        <div className="card-body">
          <h2 className="card-title text-2xl mb-4">Recommended Course</h2>
          <div className="flex items-center justify-center py-8">
            <span className="loading loading-spinner loading-lg"></span>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (error || !recommendedCourse) {
    return (
      <div className="card bg-base-100 shadow-xl border border-base-300">
        <div className="card-body">
          <h2 className="card-title text-2xl mb-4">Recommended Course</h2>
          <p className="text-base-content/70">
            {error || 'No recommendation available at this time.'}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="card bg-base-100 shadow-xl border border-base-300">
      <div className="card-body">
        {/* Header Section */}
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-4">
          <div className="flex-1">
            <div className="badge badge-primary badge-lg mb-2">Recommended for You</div>
            <h2 className="card-title text-2xl mb-2">
              <span className="text-primary">{recommendedCourse.course_code}</span>
              <span className="text-base-content"> - {recommendedCourse.course_name}</span>
            </h2>
            <p className="text-base-content/70 text-sm">
              Based on similar students' course history, this course might be a good fit for you.
            </p>
          </div>
        </div>

        {/* Divider */}
        <div className="divider my-4"></div>

        {/* Action Section */}
        <div className="card-actions justify-end">
          <Link
            href={`/result?courseId=${recommendedCourse.id}`}
            className="btn btn-primary"
          >
            Evaluate This Course
          </Link>
          <Link
            href="/courses"
            className="btn btn-outline"
          >
            View All Courses
          </Link>
        </div>
      </div>
    </div>
  );
}

