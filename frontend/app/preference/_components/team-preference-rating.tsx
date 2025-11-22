import { UseFormRegister, FieldErrors } from 'react-hook-form';
import { ErrorMessage } from './error-message';

interface TeamPreferenceRatingProps {
  register: UseFormRegister<any>;
  errors: FieldErrors;
}

export function TeamPreferenceRating({ register, errors }: TeamPreferenceRatingProps) {
  return (
    <div className="form-control space-y-4">
      <label className="label p-0">
        <span className="label-text text-lg font-semibold">Team Project Preference</span>
      </label>
      <div className="flex flex-col items-center p-6 bg-base-200/50 rounded-box gap-4">
        <div className="rating rating-lg gap-2">
          {[1, 2, 3, 4, 5].map((val) => (
            <input
              key={val}
              type="radio"
              value={val}
              className="mask mask-star-2 bg-orange-400 hover:scale-110 transition-transform"
              {...register('team_preference')}
            />
          ))}
        </div>
        <div className="flex justify-between w-full max-w-xs text-sm font-medium text-base-content/70">
          <span>Hate it 😡</span>
          <span>Love it 🤩</span>
        </div>
      </div>
      <ErrorMessage message={errors.team_preference?.message as string} />
    </div>
  );
}
