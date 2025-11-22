import { UseFormRegister, FieldErrors, UseFieldArrayReturn } from 'react-hook-form';
import { ErrorMessage } from './error-message';

interface InterestsInputProps {
  fields: UseFieldArrayReturn<any, 'interests'>['fields'];
  register: UseFormRegister<any>;
  errors: FieldErrors;
  onAppend: () => void;
  onRemove: (index: number) => void;
}

export function InterestsInput({ fields, register, errors, onAppend, onRemove }: InterestsInputProps) {
  return (
    <div className="form-control space-y-4">
      <label className="label p-0">
        <span className="label-text text-lg font-semibold">Interests & Aptitude</span>
      </label>
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
              disabled={fields.length === 1 && index === 0}
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
        onClick={onAppend}
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" /></svg>
        Add Another Interest
      </button>
    </div>
  );
}
