import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import type { UserPreferences } from "@/app/_types/preference";

const defaultExampleInterests = [
  { id: '1', value: 'Web Development', checked: false },
  { id: '2', value: 'Data Science', checked: false },
  { id: '3', value: 'AI/ML', checked: false },
  { id: '4', value: 'Mobile Dev', checked: false },
  { id: '5', value: 'UI/UX Design', checked: false },
  { id: '6', value: 'Cloud Computing', checked: false },
  { id: '7', value: 'Cybersecurity', checked: false },
  { id: '8', value: 'DevOps', checked: false },
];

export const getDefaultPreferences = (): UserPreferences => {
  return {
    eval_preference: 3,
    example_interests: defaultExampleInterests,
    interests: [],
    team_preference: 3,
    class_type: [],
    completed_courses: [],
  };
};

interface PreferencesState {
  preferences: UserPreferences | null;
  setPreferences: (prefs: UserPreferences) => void;
  clearPreferences: () => void;
  getDefaultPreferences: () => UserPreferences;
}

export const usePreferencesStore = create<PreferencesState>()(
  persist(
    (set) => ({
      preferences: null,

      setPreferences: (prefs: UserPreferences) => {
        set({ preferences: prefs });
      },

      clearPreferences: () => {
        set({ preferences: null });
      },

      getDefaultPreferences,
    }),
    {
      name: "user-preferences-storage",
      storage: createJSONStorage(() => localStorage),
    }
  )
);

