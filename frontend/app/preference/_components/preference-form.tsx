'use client';

import { useEffect } from 'react';
import { useForm, useFieldArray, type Resolver } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { FormHeader } from './form-header';
import { EvaluationPreferenceSlider } from './evaluation-preference-slider';
import { InterestsInput } from './interests-input';
import { TeamPreferenceRating } from './team-preference-rating';
import { ClassTypeSelector } from './class-type-selector';

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
});

export type FormData = z.infer<typeof schema>;

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

const getDefaultValues = (): FormData => {
  try {
    const stored = localStorage.getItem('userPreferences');
    if (stored) {
      const parsed = JSON.parse(stored) as FormData;
      return {
        ...parsed,
        example_interests: parsed.example_interests || defaultExampleInterests,
      };
    }
  } catch (error) {
    console.error('Failed to load preferences from localStorage:', error);
  }
  return {
    eval_preference: 3,
    example_interests: defaultExampleInterests,
    interests: [],
    team_preference: 3,
    class_type: [],
  };
};

export function PreferenceForm() {
  const defaultValues: FormData = {
    eval_preference: 3,
    example_interests: defaultExampleInterests,
    interests: [],
    team_preference: 3,
    class_type: [],
  };

  const {
    register,
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(schema) as Resolver<FormData>,
    defaultValues,
  });

  useEffect(() => {
    const storedData = getDefaultValues();
    reset(storedData);
  }, [reset]);

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'interests',
  });


  const onSubmit = (data: FormData) => {
    try {
      localStorage.setItem('userPreferences', JSON.stringify(data));
      console.log('Form Data saved to localStorage:', data);
      alert('Preferences saved to local storage!');
    } catch (error) {
      console.error('Failed to save preferences to localStorage:', error);
      alert('Failed to save preferences. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="card bg-base-100 shadow-xl border border-base-300 w-full max-w-3xl mx-auto overflow-hidden">
      <div className="card-body p-8 gap-8">
        <FormHeader
          title="User Preferences"
          description="Tell us about your learning style and interests"
        />

        <div className="divider"></div>

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
  );
}
