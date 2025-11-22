'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useState } from 'react';
import Link from 'next/link';
import { AuthCard } from '@/app/(auth)/_components/auth-card';
import { FormInput } from '@/components/form-input';
import { SocialLoginButton } from '@/app/(auth)/_components/social-login-button';
import { EmailIcon, PasswordIcon } from '@/app/(auth)/_components/icons';

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export function LoginForm() {
  const [isLoading, setIsLoading] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  async function onSubmit(data: LoginFormData) {
    setIsLoading(true);
    try {
      console.log('Login data:', data);
      await new Promise((resolve) => setTimeout(resolve, 1500));
      alert('Login successful!');
    } catch (error) {
      console.error('Login error:', error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <AuthCard
      title="Welcome Back"
      subtitle="Sign in to your account to continue"
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
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

        <div className="flex items-center justify-between">
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" className="checkbox checkbox-primary checkbox-sm" />
            <span className="text-sm">Remember me</span>
          </label>
          <a href="#" className="text-sm link link-primary">
            Forgot password?
          </a>
        </div>

        <button
          type="submit"
          className="btn btn-primary w-full"
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <span className="loading loading-spinner loading-sm"></span>
              Signing in...
            </>
          ) : (
            'Sign in'
          )}
        </button>
      </form>

      <div className="divider">OR</div>

      <SocialLoginButton />

      <p className="text-center text-sm mt-4">
        Don&apos;t have an account?{' '}
        <Link href="/signup" className="link link-primary font-semibold">
          Sign up
        </Link>
      </p>
    </AuthCard>
  );
}

