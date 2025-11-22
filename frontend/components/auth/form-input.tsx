import { forwardRef } from 'react';

interface FormInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  icon: React.ReactNode;
  error?: string;
}

export const FormInput = forwardRef<HTMLInputElement, FormInputProps>(
  ({ icon, error, ...props }, ref) => {
    return (
      <div>
        <label className="input input-primary flex items-center gap-2">
          {icon}
          <input ref={ref} {...props} className="grow" />
        </label>
        {error && (
          <p className="text-error text-sm mt-1 ml-1">
            {error}
          </p>
        )}
      </div>
    );
  }
);

FormInput.displayName = 'FormInput';

