import Link from 'next/link';
import { LandingFeatures } from './features';

export function LandingHero() {
  return (
    <div className="hero min-h-[calc(100vh-64px)]">
      <div className="hero-content text-center">
        <div className="max-w-2xl">
          <h1 className="text-5xl font-bold mb-8">
            Welcome to REALThon
          </h1>
          <p className="text-lg mb-8 text-base-content/70">
            Experience a modern authentication system built with Next.js, daisyUI, and best practices.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link href="/login" className="btn btn-primary btn-lg">
              Get Started
            </Link>
            <a href="https://daisyui.com" target="_blank" rel="noopener noreferrer" className="btn btn-outline btn-lg">
              Learn More
            </a>
          </div>
          
          <div className="divider my-12"></div>
          
          <LandingFeatures />
        </div>
      </div>
    </div>
  );
}
