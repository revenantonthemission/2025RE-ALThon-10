import { UseFormRegister, FieldErrors } from 'react-hook-form';
import { ErrorMessage } from './error-message';

interface TeamPreferenceRatingProps {
  register: UseFormRegister<any>;
  errors: FieldErrors;
}

export function TeamPreferenceRating({ register, errors }: TeamPreferenceRatingProps) {
  return (
    <div className="form-control space-y-4">
      <div className="flex justify-between items-end">
        <label className="label p-0">
          <span className="label-text text-lg font-semibold">Team Project Preference</span>
        </label>
        <span className="badge badge-ghost font-mono text-xs">1: Hate it - 5: Love it</span>
      </div>

      <div className="p-6 bg-base-200/50 rounded-box">
        <input
          type="range"
          min="1"
          max="5"
          step="1"
          className="range range-primary range-lg w-full"
          {...register('team_preference')}
        />
        <div className="w-full flex justify-between px-2 mt-3 font-bold text-base-content/60">
          <span className="text-[10px] sm:text-xs">
            <span className="hidden sm:inline">Hate it </span>😡
          </span>
          <span className="hidden sm:inline text-xs">|</span>
          <span className="text-[10px] sm:text-xs">Neutral</span>
          <span className="hidden sm:inline text-xs">|</span>
          <span className="text-[10px] sm:text-xs">
            <span className="hidden sm:inline">Love it </span>🤩
          </span>
        </div>
      </div>
      <ErrorMessage message={errors.team_preference?.message as string} />
    </div>
  );
}
