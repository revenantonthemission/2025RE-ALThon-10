'use client';

import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { FormHeader } from './form-header';
import { EvaluationPreferenceSlider } from './evaluation-preference-slider';
import { InterestsInput } from './interests-input';
import { TeamPreferenceRating } from './team-preference-rating';
import { ClassTypeSelector } from './class-type-selector';

const schema = z.object({
  eval_preference: z.coerce.number().min(1).max(5),
  interests: z.array(z.object({ value: z.string().min(1, 'Required') })).min(1, 'At least one interest is required'),
  team_preference: z.coerce.number().min(1).max(5),
  class_type: z.array(z.string()).min(1, 'Select at least one option'),
});

type FormData = z.infer<typeof schema>;

export function PreferenceForm() {
  const {
    register,
    control,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(schema),
    defaultValues: {
      eval_preference: 3,
      interests: [{ value: '' }],
      team_preference: 3,
      class_type: [],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'interests',
  });

  const onSubmit = (data: FormData) => {
    console.log('Form Data:', data);
    // TODO: Send data to backend
    alert('Preferences saved! (Check console for data)');
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
          errors={errors}
          onAppend={() => append({ value: '' })}
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
