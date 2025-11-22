'use client';

import { useMemo } from 'react';
import Link from 'next/link';
import { RadarChart, type RadarChartData } from './_components/radar-chart';
import { usePreferencesStore } from '@/app/_stores/preferences';

export default function ResultPage() {
  const preferences = usePreferencesStore((state) => state.preferences);

  const chartData = useMemo<RadarChartData | null>(() => {
    if (!preferences) return null;

    // Generate chart data from preferences
    // Colors will be applied by RadarChart component based on theme
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
            (preferences.eval_preference / 5) * 100, // Convert 1-5 scale to 0-100
            (preferences.team_preference / 5) * 100, // Convert 1-5 scale to 0-100
            Math.min((preferences.interests?.length || 0) * 20, 100), // Interests count (max 5 = 100)
            Math.min((preferences.class_type?.length || 0) * 33.33, 100), // Class types (max 3 = 100)
            ((preferences.eval_preference + preferences.team_preference) / 10) * 100, // Average engagement
            (preferences.team_preference / 5) * 100, // Collaboration score
          ],
          // Colors will be automatically applied by RadarChart component based on theme
        },
      ],
    };
  }, [preferences]);

  if (!preferences || !chartData) {
    return (
      <div className="min-h-screen bg-base-200 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="card bg-base-100 shadow-xl border border-base-300 w-full max-w-3xl mx-auto">
          <div className="card-body">
            <h2 className="card-title text-2xl mb-4">No Preferences Found</h2>
            <p className="text-base-content/70 mb-4">
              Please complete the preference form first to see your results.
            </p>
            <div className="card-actions">
              <a href="/preference" className="btn btn-primary">
                Go to Preferences
              </a>
            </div>
          </div>
        </div>
      </div>
    );
  }

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
            <RadarChart data={chartData} title="Preference Analysis" />
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

