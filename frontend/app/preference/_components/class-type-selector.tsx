import { UseFormRegister, FieldErrors } from 'react-hook-form';
import { ErrorMessage } from './error-message';

interface ClassTypeSelectorProps {
  register: UseFormRegister<any>;
  errors: FieldErrors;
  options?: string[];
}

const DEFAULT_OPTIONS = ['In-Person', 'Online (Zoom)', 'Recorded', 'Hybrid'];

export function ClassTypeSelector({ register, errors, options = DEFAULT_OPTIONS }: ClassTypeSelectorProps) {
  return (
    <div className="form-control space-y-4">
      <label className="label p-0">
        <span className="label-text text-lg font-semibold">Preferred Class Mode</span>
      </label>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {options.map((type) => (
          <label key={type} className="label cursor-pointer border border-base-300 rounded-lg p-4 hover:border-primary hover:bg-base-200 transition-all has-[:checked]:border-primary has-[:checked]:bg-primary/5 has-[:checked]:shadow-sm">
            <span className="label-text font-medium">{type}</span>
            <input
              type="checkbox"
              value={type}
              className="checkbox checkbox-primary"
              {...register('class_type')}
            />
          </label>
        ))}
      </div>
      <ErrorMessage message={errors.class_type?.message as string} />
    </div>
  );
}
