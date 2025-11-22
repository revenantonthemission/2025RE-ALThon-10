import { usePreferencesStore } from "@/app/_stores/preferences";
import type { UserPreferences } from "@/app/_types/preference";

/**
 * Custom hook for user preferences operations
 * Provides convenient access to preferences state and actions
 *
 * @example
 * ```tsx
 * import { usePreferences } from '@/app/_hooks/usePreferences';
 *
 * function MyComponent() {
 *   const { preferences, setPreferences, hasPreferences } = usePreferences();
 *
 *   if (!hasPreferences) {
 *     return <div>Please set your preferences</div>;
 *   }
 *
 *   return (
 *     <div>
 *       <h1>Your Preferences</h1>
 *       <button onClick={() => setPreferences(newPrefs)}>Update</button>
 *     </div>
 *   );
 * }
 * ```
 */
export function usePreferences() {
  const store = usePreferencesStore();

  return {
    // Preferences state
    preferences: store.preferences,
    hasPreferences: store.preferences !== null,

    // Preferences actions
    setPreferences: store.setPreferences,
    clearPreferences: store.clearPreferences,
    getDefaultPreferences: store.getDefaultPreferences,

    // Helper functions
    getPreferences: (): UserPreferences | null => store.preferences,
  };
}

