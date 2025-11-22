'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useState } from 'react';
import Link from 'next/link';
import { AuthCard } from '@/components/auth/auth-card';
import { FormInput } from '@/components/auth/form-input';
import { SocialLoginButton } from '@/components/auth/social-login-button';
import { EmailIcon, PasswordIcon, UserIcon } from '@/components/auth/icons';

const signupSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string().min(8, 'Please confirm your password'),
  terms: z.boolean().refine((val) => val === true, {
    message: 'You must accept the terms and conditions',
  }),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type SignupFormData = z.infer<typeof signupSchema>;

export function SignupForm() {
  const [isLoading, setIsLoading] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
  });

  async function onSubmit(data: SignupFormData) {
    setIsLoading(true);
    try {
      console.log('Signup data:', data);
      await new Promise((resolve) => setTimeout(resolve, 1500));
      alert('Account created successfully!');
    } catch (error) {
      console.error('Signup error:', error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <AuthCard
      title="Create Account"
      subtitle="Sign up to get started with REALThon"
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <FormInput
          type="text"
          placeholder="Full name"
          icon={<UserIcon />}
          error={errors.name?.message}
          {...register('name')}
        />

        <FormInput
          type="email"
          placeholder="Email address"
          icon={<EmailIcon />}
          error={errors.email?.message}
          {...register('email')}
        />

        <FormInput
          type="password"
          placeholder="Password"
          icon={<PasswordIcon />}
          error={errors.password?.message}
          {...register('password')}
        />

        <FormInput
          type="password"
          placeholder="Confirm password"
          icon={<PasswordIcon />}
          error={errors.confirmPassword?.message}
          {...register('confirmPassword')}
        />

        <div>
          <label className="flex items-start gap-3 cursor-pointer">
            <input
              type="checkbox"
              className="checkbox checkbox-primary mt-1"
              {...register('terms')}
            />
            <span className="text-sm">
              I agree to the{' '}
              <a href="#" className="link link-primary">
                Terms and Conditions
              </a>{' '}
              and{' '}
              <a href="#" className="link link-primary">
                Privacy Policy
              </a>
            </span>
          </label>
          {errors.terms && (
            <p className="text-error text-sm mt-1 ml-1">
              {errors.terms.message}
            </p>
          )}
        </div>

        <button
          type="submit"
          className="btn btn-primary w-full"
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <span className="loading loading-spinner loading-sm"></span>
              Creating account...
            </>
          ) : (
            'Sign up'
          )}
        </button>
      </form>

      <div className="divider">OR</div>

      <SocialLoginButton />

      <p className="text-center text-sm mt-4">
        Already have an account?{' '}
        <Link href="/login" className="link link-primary font-semibold">
          Sign in
        </Link>
      </p>
    </AuthCard>
  );
}

