'use client';

import { useState, useMemo, useRef, useEffect } from 'react';
import { useFormContext, Controller } from 'react-hook-form';
import useSWR from 'swr';
import { getCourses } from '@/app/_lib/api/courses';
import { Course } from '@/app/_types/course';
import { FormData } from './preference-form';

interface CompletedCourse {
  id: string;
  grade: string;
}

export function CourseSelection() {
  const { control, formState: { errors } } = useFormContext<FormData>();
  const [searchQuery, setSearchQuery] = useState('');
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Fetch courses using SWR
  const { data: courses = [], isLoading, error } = useSWR<Course[]>(
    'courses',
    getCourses,
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: false,
    }
  );

  // Filter courses based on search query
  const filteredCourses = useMemo(() => {
    if (!searchQuery.trim()) {
      return courses;
    }
    const query = searchQuery.toLowerCase();
    return courses.filter(
      (course) =>
        course.course_name.toLowerCase().includes(query) ||
        course.course_code.toLowerCase().includes(query)
    );
  }, [courses, searchQuery]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsDropdownOpen(false);
      }
    };

    if (isDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isDropdownOpen]);

  return (
    <div className="form-control w-full">
      <label className="label">
        <span className="label-text text-lg font-semibold">
          수강완료한 강의 (Completed Courses)
        </span>
      </label>
      <p className="text-sm text-base-content/70 mb-4">
        검색하여 수강 완료한 강의를 선택하세요 (Search and select completed courses)
      </p>

      <Controller
        name="completed_courses"
        control={control}
        rules={{ required: 'At least one course is required' }}
        render={({ field }) => {
          const selectedCourses = (field.value || []) as CompletedCourse[];
          
          const handleCourseToggle = (course: Course) => {
            const courseId = course.id.toString();
            const isSelected = selectedCourses.some((c) => c.id === courseId);
            
            if (isSelected) {
              // Remove course
              field.onChange(
                selectedCourses.filter((c) => c.id !== courseId)
              );
            } else {
              // Add course with default grade
              field.onChange([
                ...selectedCourses,
                { id: courseId, grade: 'A' },
              ]);
            }
          };

          const handleGradeChange = (courseId: string, grade: string) => {
            field.onChange(
              selectedCourses.map((c) =>
                c.id === courseId ? { ...c, grade } : c
              )
            );
          };

          const handleRemoveCourse = (courseId: string) => {
            field.onChange(selectedCourses.filter((c) => c.id !== courseId));
          };

          return (
            <div className="space-y-4" ref={dropdownRef}>
              {/* Search Input */}
              <div className="relative">
                <input
                  type="text"
                  placeholder="강의명 또는 강의코드로 검색 (Search by course name or code)"
                  className="input input-bordered w-full pr-10"
                  value={searchQuery}
                  onChange={(e) => {
                    setSearchQuery(e.target.value);
                    setIsDropdownOpen(true);
                  }}
                  onFocus={() => setIsDropdownOpen(true)}
                  disabled={isLoading}
                />
                {isLoading && (
                  <span className="loading loading-spinner loading-sm absolute right-3 top-1/2 -translate-y-1/2"></span>
                )}
                {!isLoading && searchQuery && (
                  <button
                    type="button"
                    className="absolute right-3 top-1/2 -translate-y-1/2 btn btn-ghost btn-xs btn-circle"
                    onClick={() => {
                      setSearchQuery('');
                      setIsDropdownOpen(false);
                    }}
                  >
                    ✕
                  </button>
                )}
              </div>

              {/* Error Message */}
              {errors.completed_courses && (
                <div className="alert alert-error">
                  <span>{errors.completed_courses.message}</span>
                </div>
              )}

              {/* API Error */}
              {error && (
                <div className="alert alert-error">
                  <span>Failed to load courses. Please try again later.</span>
                </div>
              )}

              {/* Dropdown Results */}
              {isDropdownOpen && searchQuery && filteredCourses.length > 0 && (
                <div className="card bg-base-200 border border-base-300 max-h-64 overflow-y-auto relative z-20">
                  <div className="card-body p-2">
                    <ul className="menu menu-compact">
                      {filteredCourses.slice(0, 20).map((course) => {
                        const isSelected = selectedCourses.some(
                          (c) => c.id === course.id.toString()
                        );
                        return (
                          <li key={course.id}>
                            <button
                              type="button"
                              className={isSelected ? 'active' : ''}
                              onClick={() => {
                                handleCourseToggle(course);
                                setSearchQuery('');
                                setIsDropdownOpen(false);
                              }}
                            >
                              <div className="flex flex-col items-start">
                                <span className="font-semibold">
                                  {course.course_name}
                                </span>
                                <span className="text-xs text-base-content/70">
                                  {course.course_code}
                                </span>
                              </div>
                              {isSelected && (
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  className="h-5 w-5"
                                  fill="none"
                                  viewBox="0 0 24 24"
                                  stroke="currentColor"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth="2"
                                    d="M5 13l4 4L19 7"
                                  />
                                </svg>
                              )}
                            </button>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                </div>
              )}

              {/* No Results */}
              {isDropdownOpen &&
                searchQuery &&
                !isLoading &&
                filteredCourses.length === 0 && (
                  <div className="alert alert-info relative z-20">
                    <span>No courses found matching &quot;{searchQuery}&quot;</span>
                  </div>
                )}

              {/* Selected Courses List */}
              {selectedCourses.length > 0 && (
                <div className="space-y-2">
                  <label className="label">
                    <span className="label-text font-medium">
                      선택된 강의 ({selectedCourses.length})
                    </span>
                  </label>
                  <div className="space-y-2">
                    {selectedCourses.map((completedCourse) => {
                      const course = courses.find(
                        (c) => c.id.toString() === completedCourse.id
                      );
                      if (!course) return null;

                      return (
                        <div
                          key={completedCourse.id}
                          className="card bg-base-200 border border-base-300"
                        >
                          <div className="card-body p-4">
                            <div className="flex items-center justify-between gap-4">
                              <div className="flex-1">
                                <h3 className="font-semibold">
                                  {course.course_name}
                                </h3>
                                <p className="text-sm text-base-content/70">
                                  {course.course_code}
                                </p>
                              </div>
                              <div className="flex items-center gap-2">
                                <select
                                  className="select select-bordered select-sm w-20"
                                  value={completedCourse.grade}
                                  onChange={(e) =>
                                    handleGradeChange(
                                      completedCourse.id,
                                      e.target.value
                                    )
                                  }
                                >
                                  <option value="A+">A+</option>
                                  <option value="A">A</option>
                                  <option value="B+">B+</option>
                                  <option value="B">B</option>
                                  <option value="C+">C+</option>
                                  <option value="C">C</option>
                                  <option value="D+">D+</option>
                                  <option value="D">D</option>
                                  <option value="F">F</option>
                                </select>
                                <button
                                  type="button"
                                  className="btn btn-ghost btn-sm btn-circle"
                                  onClick={() =>
                                    handleRemoveCourse(completedCourse.id)
                                  }
                                >
                                  ✕
                                </button>
                              </div>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

            </div>
          );
        }}
      />
    </div>
  );
}

