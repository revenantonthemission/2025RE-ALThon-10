import { UseFormRegister, FieldErrors } from 'react-hook-form';
import { ErrorMessage } from './error-message';

interface EvaluationPreferenceSliderProps {
  register: UseFormRegister<any>;
  errors: FieldErrors;
}

export function EvaluationPreferenceSlider({ register, errors }: EvaluationPreferenceSliderProps) {
  return (
    <div className="form-control space-y-4">
      <div className="flex justify-between items-end">
        <label className="label p-0">
          <span className="label-text text-lg font-semibold">Evaluation Preference</span>
        </label>
        <span className="badge badge-ghost font-mono text-xs">1: Exam - 5: Assignment</span>
      </div>

      <div className="p-6 bg-base-200/50 rounded-box">
        <input
          type="range"
          min="1"
          max="5"
          step="1"
          className="range range-primary range-lg w-full"
          {...register('eval_preference')}
        />
        <div className="w-full flex justify-between px-2 mt-3 font-bold text-base-content/60">
          <span className="text-[10px] sm:text-xs">
            <span className="hidden sm:inline">Exam </span>Focused
          </span>
          <span className="hidden sm:inline text-xs">|</span>
          <span className="text-[10px] sm:text-xs">Balanced</span>
          <span className="hidden sm:inline text-xs">|</span>
          <span className="text-[10px] sm:text-xs">
            <span className="hidden sm:inline">Assignment </span>Focused
          </span>
        </div>
      </div>
      <ErrorMessage message={errors.eval_preference?.message as string} />
    </div>
  );
}
