'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { LandingNavbar } from '@/components/navbar';
import Link from 'next/link';

type PreferenceData = {
  eval_preference: number;
  example_interests: Array<{ id: string; value: string; checked?: boolean }>;
  interests: Array<{ value: string }>;
  team_preference: number;
  class_type: string[];
};

export default function Home() {
  const router = useRouter();
  const [preferences, setPreferences] = useState<PreferenceData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    try {
      const stored = localStorage.getItem('userPreferences');
      if (stored) {
        const parsed = JSON.parse(stored) as PreferenceData;
        setPreferences(parsed);
      } else {
        router.push('/preference');
      }
    } catch (error) {
      console.error('Failed to load preferences:', error);
      router.push('/preference');
    } finally {
      setIsLoading(false);
    }
  }, [router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-base-200 flex items-center justify-center">
        <span className="loading loading-spinner loading-lg"></span>
      </div>
    );
  }

  if (!preferences) {
    return null; // Will redirect
  }

  return (
    <div className="min-h-screen bg-base-200">
      <LandingNavbar />
      <div className="container mx-auto px-4 py-12">
        <div className="card bg-base-100 shadow-xl border border-base-300 w-full max-w-4xl mx-auto">
          <div className="card-body p-8 gap-6">
            <div className="flex justify-between items-center">
              <h2 className="card-title text-3xl">Your Preferences</h2>
              <Link href="/preference" className="btn btn-outline btn-sm">
                Edit Preferences
              </Link>
            </div>

            <div className="divider"></div>

            <div className="grid gap-6 md:grid-cols-2">
              <div className="stat bg-base-200 rounded-lg">
                <div className="stat-title">Evaluation Preference</div>
                <div className="stat-value text-2xl">{preferences.eval_preference}/5</div>
                <div className="stat-desc">Your preferred evaluation style</div>
              </div>

              <div className="stat bg-base-200 rounded-lg">
                <div className="stat-title">Team Preference</div>
                <div className="stat-value text-2xl">{preferences.team_preference}/5</div>
                <div className="stat-desc">Your team collaboration preference</div>
              </div>
            </div>

            <div className="card bg-base-200">
              <div className="card-body p-6">
                <h3 className="card-title text-lg mb-4">Your Interests</h3>
                <div className="flex flex-wrap gap-2">
                  {preferences.interests.map((interest, index) => (
                    <span key={index} className="badge badge-primary badge-lg">
                      {interest.value}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="card bg-base-200">
              <div className="card-body p-6">
                <h3 className="card-title text-lg mb-4">Class Types</h3>
                <div className="flex flex-wrap gap-2">
                  {preferences.class_type.map((type, index) => (
                    <span key={index} className="badge badge-secondary badge-lg">
                      {type}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
