import { UseFormRegister, FieldErrors, UseFieldArrayReturn, Control, useWatch } from 'react-hook-form';
import { ErrorMessage } from './error-message';
import type { FormData } from './preference-form';

const EXAMPLE_INTERESTS = [
  "Web Development",
  "Data Science",
  "AI/ML",
  "Mobile Dev",
  "UI/UX Design",
  "Cloud Computing",
  "Cybersecurity",
  "DevOps"
];

interface InterestsInputProps {
  fields: UseFieldArrayReturn<FormData, 'interests'>['fields'];
  register: UseFormRegister<FormData>;
  control: Control<FormData>;
  errors: FieldErrors<FormData>;
  onAppend: (value?: { value: string }) => void;
  onRemove: (index: number) => void;
}

export function InterestsInput({ fields, register, control, errors, onAppend, onRemove }: InterestsInputProps) {
  const watchedInterests = useWatch({
    control,
    name: 'interests',
  });

  const currentInterests = watchedInterests?.map((item) => item.value) || [];

  const toggleInterest = (interest: string) => {
    const index = currentInterests.findIndex((val: string) => val === interest);
    if (index !== -1) {
      onRemove(index);
    } else {
      const emptyIndex = currentInterests.findIndex((val: string) => val === '');
      if (emptyIndex !== -1) {
        onRemove(emptyIndex);
      }
      onAppend({ value: interest });
    }
  };

  return (
    <div className="form-control space-y-4">
      <label className="label p-0">
        <span className="label-text text-lg font-semibold">Interests & Aptitude</span>
      </label>

      <div className="flex flex-wrap gap-2 mb-2">
        {EXAMPLE_INTERESTS.map((interest) => {
          const isSelected = currentInterests.includes(interest);
          return (
            <button
              key={interest}
              type="button"
              className={`btn btn-sm ${isSelected ? 'btn-primary' : 'btn-outline'}`}
              onClick={() => toggleInterest(interest)}
            >
              {interest}
              {isSelected && (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              )}
            </button>
          );
        })}
      </div>

      <div className="space-y-3">
        {fields.map((field, index) => (
          <div key={field.id} className="join w-full">
            <input
              type="text"
              placeholder="E.g., Web Development, AI, Data Science"
              className="input input-bordered join-item w-full focus:outline-none focus:border-primary"
              {...register(`interests.${index}.value` as const)}
            />
            <button
              type="button"
              className="btn btn-square join-item btn-outline btn-error hover:bg-error hover:text-error-content transition-colors"
              onClick={() => onRemove(index)}
              disabled={false}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
            </button>
          </div>
        ))}
      </div>
      <ErrorMessage message={(errors.interests?.message || errors.interests?.root?.message) as string} />
      <button
        type="button"
        className="btn btn-ghost btn-sm gap-2 self-start text-primary hover:bg-primary/10"
        onClick={() => onAppend({ value: '' })}
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" /></svg>
        Add Another Interest
      </button>
    </div>
  );
}
