import { LandingNavbar } from '@/components/landing/navbar';
import { LandingHero } from '@/components/landing/hero';

export default function Home() {
  return (
    <div className="min-h-screen bg-base-200">
      <LandingNavbar />
      <LandingHero />
    </div>
  );
}
