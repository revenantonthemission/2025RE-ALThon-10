'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useForm, useFieldArray, FormProvider, type Resolver } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { FormHeader } from './form-header';
import { EvaluationPreferenceSlider } from './evaluation-preference-slider';
import { InterestsInput } from './interests-input';
import { TeamPreferenceRating } from './team-preference-rating';
import { ClassTypeSelector } from './class-type-selector';
import { CourseSelection } from './course-selection';
import type { UserPreferences } from '@/app/_types/preference';
import { usePreferencesStore } from '@/app/_stores/preferences';

const schema = z.object({
  eval_preference: z.coerce.number().min(1).max(5),
  example_interests: z.array(z.object({
    id: z.string(),
    value: z.string(),
    checked: z.boolean().optional(),
  })),
  interests: z.array(z.object({ value: z.string().min(1, 'Required') })).min(1, 'At least one interest is required'),
  team_preference: z.coerce.number().min(1).max(5),
  class_type: z.array(z.string()).min(1, 'Select at least one option'),
  completed_courses: z.array(z.object({
    id: z.string(),
    grade: z.string(),
  })).min(1, 'At least one completed course is required'),
});

export type FormData = z.infer<typeof schema>;

// FormData is the same as UserPreferences, but we keep both for clarity
// FormData is used for form validation, UserPreferences for localStorage
export type { UserPreferences };


export function PreferenceForm() {
  const router = useRouter();
  const { preferences, setPreferences, getDefaultPreferences } = usePreferencesStore();
  
  const defaultValues: FormData = preferences || getDefaultPreferences();

  const methods = useForm<FormData>({
    resolver: zodResolver(schema) as Resolver<FormData>,
    defaultValues,
  });

  const {
    register,
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = methods;

  useEffect(() => {
    const storedData = preferences || getDefaultPreferences();
    reset(storedData);
  }, [reset, preferences, getDefaultPreferences]);

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'interests',
  });


  const onSubmit = (data: FormData) => {
    try {
      setPreferences(data);
      console.log('Form Data saved:', data);
      router.push('/result');
    } catch (error) {
      console.error('Failed to save preferences:', error);
      alert('Failed to save preferences. Please try again.');
    }
  };

  return (
    <FormProvider {...methods}>
      <form onSubmit={handleSubmit(onSubmit)} className="card bg-base-100 shadow-xl border border-base-300 w-full max-w-3xl mx-auto overflow-hidden">
        <div className="card-body p-8 gap-8">
          <FormHeader
            title="User Preferences"
            description="Tell us about your learning style and interests"
          />

          <div className="divider"></div>

          <CourseSelection />

          <EvaluationPreferenceSlider
            register={register}
            errors={errors}
          />

          <InterestsInput
            fields={fields}
            register={register}
            control={control}
            errors={errors}
            onAppend={(value) => append(value || { value: '' })}
            onRemove={remove}
          />

          <TeamPreferenceRating
            register={register}
            errors={errors}
          />

          <ClassTypeSelector
            register={register}
            errors={errors}
          />

          <div className="card-actions justify-end mt-8">
            <button type="submit" className="btn btn-primary btn-lg w-full sm:w-auto shadow-lg hover:shadow-primary/40 transition-shadow">
              Save Preferences
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" /></svg>
            </button>
          </div>
        </div>
      </form>
    </FormProvider>
  );
}
