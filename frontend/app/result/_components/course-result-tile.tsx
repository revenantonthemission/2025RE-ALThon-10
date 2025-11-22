'use client';

import { RadarChart, type RadarChartData } from './radar-chart';

/**
 * Course information interface
 * Represents the basic course data to display in the tile
 */
export interface CourseInfo {
  course_code: string;
  course_name: string;
  professor?: string;
  credits?: number;
  department?: string;
  major?: string;
}

/**
 * Props for the CourseResultTile component
 */
interface CourseResultTileProps {
  /** Course information to display */
  course: CourseInfo;
  /** Radar chart data for visualizing course match/analysis */
  chartData: RadarChartData;
  /** Optional title for the radar chart (defaults to course name) */
  chartTitle?: string;
  /** Optional match score or compatibility percentage */
  matchScore?: number;
  /** Optional description or summary of the course */
  description?: string;
}

/**
 * CourseResultTile Component
 * 
 * A card-based tile component that displays course information along with
 * a radar chart visualization. This component is designed to show course
 * recommendations or analysis results in a visually appealing format.
 * 
 * Features:
 * - Course metadata display (code, name, professor, credits)
 * - Radar chart visualization for multi-dimensional analysis
 * - Match score indicator (if provided)
 * - Responsive design using daisyUI card components
 * 
 * @param props - Component props containing course info and chart data
 * @returns JSX element representing the course result tile
 */
export function CourseResultTile({
  course,
  chartData,
  chartTitle,
  matchScore,
  description,
}: CourseResultTileProps) {
  // Use provided chart title or default to course name
  const displayChartTitle = chartTitle || course.course_name;

  return (
    <div className="card bg-base-100 shadow-xl border border-base-300 w-full">
      <div className="card-body">
        {/* Course Header Section */}
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-4">
          <div className="flex-1">
            {/* Course Code and Name */}
            <h2 className="card-title text-2xl mb-2">
              <span className="text-primary">{course.course_code}</span>
              <span className="text-base-content"> - {course.course_name}</span>
            </h2>

            {/* Course Metadata */}
            <div className="flex flex-wrap gap-4 text-sm text-base-content/70">
              {course.professor && (
                <div className="flex items-center gap-1">
                  <span className="font-semibold">Professor:</span>
                  <span>{course.professor}</span>
                </div>
              )}
              {course.credits && (
                <div className="flex items-center gap-1">
                  <span className="font-semibold">Credits:</span>
                  <span>{course.credits}</span>
                </div>
              )}
              {course.department && (
                <div className="flex items-center gap-1">
                  <span className="font-semibold">Department:</span>
                  <span>{course.department}</span>
                </div>
              )}
            </div>
          </div>

          {/* Match Score Badge (if provided) */}
          {/* {matchScore !== undefined && (
            <div className="stat bg-base-200 rounded-lg p-4 min-w-[120px]">
              <div className="stat-title text-xs">Match Score</div>
              <div className="stat-value text-2xl text-primary">
                {Math.round(matchScore)}%
              </div>
            </div>
          )} */}
        </div>

        {/* Description Section (if provided) */}
        {description && (
          <div className="mb-4">
            <p className="text-base-content/80 text-sm leading-relaxed">
              {description}
            </p>
          </div>
        )}

        {/* Divider */}
        <div className="divider my-4"></div>

        {/* Radar Chart Section */}
        <div className="w-full">
          <RadarChart data={chartData} title={displayChartTitle} />
        </div>
      </div>
    </div>
  );
}


